# superior/issue_factory.py

from django.db import transaction
from superior.models import Issue, IssueType, IssueSeverity
from kct.models import KCTEntry
from judging.models import JudgeScoreSheet


def _clear_auto_issues(team_entry):
    """
    Remove auto-created issues so we can regenerate them.
    If you later add manual issues, tag them and exclude here.
    """
    Issue.objects.filter(team_entry=team_entry).delete()


def create_kct_issues(team_entry):
    kcts = list(KCTEntry.objects.filter(team_entry=team_entry))
    if not kcts:
        return

    ruleset = getattr(team_entry.meet, "ruleset", None)
    if not ruleset:
        return

    k1 = kcts[0] if len(kcts) > 0 else None
    k2 = kcts[1] if len(kcts) > 1 else None

    division = team_entry.division  # "JAZZ" or "KICK"
    is_varsity = team_entry.team.level == "VARSITY" if hasattr(team_entry.team, "level") else True

    # ---------------------------------------------------------
    # 1. UNANIMOUS KCT-ONLY DEDUCTIONS
    # ---------------------------------------------------------
    if k1 and k2:

        # --- Timing violations ---
        if division == "JAZZ":
            min_time = ruleset.jazz_min_time
            max_time = ruleset.jazz_max_time
        else:
            min_time = ruleset.kick_min_time
            max_time = ruleset.kick_max_time

        k1_time_bad = not (min_time <= k1.routine_time_seconds <= max_time)
        k2_time_bad = not (min_time <= k2.routine_time_seconds <= max_time)

        if k1_time_bad and k2_time_bad:
            Issue.objects.create(
                team_entry=team_entry,
                issue_type=IssueType.TIME,
                severity=IssueSeverity.POTENTIAL_DEDUCTION,
                description=f"Both KCTs reported time outside allowed range ({min_time}-{max_time} seconds).",
            )

        # --- Kick count unanimous violation (Kick only) ---
        if division == "KICK" and k1.kick_count is not None and k2.kick_count is not None:
            k1_bad = not (ruleset.kick_min_count <= k1.kick_count <= ruleset.kick_max_count)
            k2_bad = not (ruleset.kick_min_count <= k2.kick_count <= ruleset.kick_max_count)

            if k1_bad and k2_bad:
                Issue.objects.create(
                    team_entry=team_entry,
                    issue_type=IssueType.KICK,
                    severity=IssueSeverity.POTENTIAL_DEDUCTION,
                    description=f"Both KCTs reported kick count outside allowed range ({ruleset.kick_min_count}-{ruleset.kick_max_count}).",
                )

        # --- Competitor count unanimous violation (Varsity only) ---
        if is_varsity:
            if division == "JAZZ":
                max_comp = ruleset.varsity_jazz_max_competitors
            else:
                max_comp = ruleset.varsity_kick_max_competitors

            min_comp = ruleset.varsity_min_competitors

            k1_bad = not (min_comp <= k1.num_competitors <= max_comp)
            k2_bad = not (min_comp <= k2.num_competitors <= max_comp)

            if k1_bad and k2_bad:
                Issue.objects.create(
                    team_entry=team_entry,
                    issue_type=IssueType.COMPETITOR,
                    severity=IssueSeverity.POTENTIAL_DEDUCTION,
                    description=f"Both KCTs reported competitor count outside Varsity range ({min_comp}-{max_comp}).",
                )

        # --- Jazz turn/leap unanimous missing ---
        if division == "JAZZ":
            if not k1.jazz_team_turn_performed and not k2.jazz_team_turn_performed:
                Issue.objects.create(
                    team_entry=team_entry,
                    issue_type=IssueType.OTHER,
                    severity=IssueSeverity.POTENTIAL_DEDUCTION,
                    description="Both KCTs reported missing Jazz turn.",
                )
            if not k1.jazz_team_leap_jump_performed and not k2.jazz_team_leap_jump_performed:
                Issue.objects.create(
                    team_entry=team_entry,
                    issue_type=IssueType.OTHER,
                    severity=IssueSeverity.POTENTIAL_DEDUCTION,
                    description="Both KCTs reported missing Jazz leap/jump.",
                )

    # ---------------------------------------------------------
    # 2. PANEL-MAJORITY CANDIDATES (KCT flags only)
    # ---------------------------------------------------------
    falls_flag = any(k.falls_observed for k in kcts)
    dangerous_flag = any(k.dangerous_move_observed for k in kcts)

    if falls_flag:
        Issue.objects.create(
            team_entry=team_entry,
            issue_type=IssueType.FALL,
            severity=IssueSeverity.POTENTIAL_DEDUCTION,
            description="Fall observed by at least one KCT.",
        )

    if dangerous_flag:
        Issue.objects.create(
            team_entry=team_entry,
            issue_type=IssueType.DANGEROUS_MOVE,
            severity=IssueSeverity.POTENTIAL_DEDUCTION,
            description="Dangerous move observed by at least one KCT.",
        )



KEYWORDS = {
    "illegal": IssueType.ILLEGAL_SKILL,
    "dangerous": IssueType.DANGEROUS_MOVE,
    "fall": IssueType.FALL,
    "safety": IssueType.SAFETY,
    "prop": IssueType.OTHER,
    "uniform": IssueType.OTHER,
}


def create_judging_issues(team_entry):
    sheets = list(JudgeScoreSheet.objects.filter(team_entry=team_entry))

    if not sheets:
        Issue.objects.create(
            team_entry=team_entry,
            issue_type=IssueType.OTHER,
            severity=IssueSeverity.WARNING,
            description="No judge score sheets submitted for this routine.",
        )
        return

    # Collect judges who flagged each keyword
    keyword_hits = {key: [] for key in KEYWORDS.keys()}

    for sheet in sheets:
        text = (sheet.comments or "").lower()
        if not text:
            continue

        for word in KEYWORDS.keys():
            if word in text:
                keyword_hits[word].append((sheet.judge, sheet.comments))

    # Create ONE issue per keyword, listing all judges who flagged it
    for word, hits in keyword_hits.items():
        if not hits:
            continue

        issue_type = KEYWORDS[word]

        judge_list = ", ".join(str(judge) for judge, _ in hits)

        # Combine all comments into a readable block
        comment_block = "\n".join(
            f"- {judge}: {comment}" for judge, comment in hits
        )

        Issue.objects.create(
            team_entry=team_entry,
            issue_type=issue_type,
            severity=IssueSeverity.POTENTIAL_DEDUCTION,
            description=(
                f"{len(hits)} judge(s) flagged '{word}'.\n"
                f"Judges: {judge_list}\n\n"
                f"Comments:\n{comment_block}"
            ),
        )


@transaction.atomic
def regenerate_issues_for_entry(team_entry):
    """
    Main entry point: clear auto issues and rebuild from KCT + Judging.
    Call this from signals.
    """
    _clear_auto_issues(team_entry)
    create_kct_issues(team_entry)
    create_judging_issues(team_entry)
