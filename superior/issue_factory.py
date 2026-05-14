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
    """
    KCT-only logic:
    - unanimous KCT for kicks/time/turn/leap/competitor
    - falls/dangerous move → panel-majority candidate (flag as potential)
    """
    kcts = list(KCTEntry.objects.filter(team_entry=team_entry))
    if not kcts:
        return

    # For convenience
    k1 = kcts[0] if len(kcts) > 0 else None
    k2 = kcts[1] if len(kcts) > 1 else None

    # Unanimous KCT-only deductions (if both present)
    if k1 and k2:
        # Example: time violation (you’ll plug in your actual rule)
        # Here we just show the pattern:
        # if k1.routine_time_seconds > limit and k2.routine_time_seconds > limit:
        #     Issue.objects.create(...)

        # Kick count violation (Kick division, both over/under limit)
        # Same idea: you’ll plug in your actual thresholds.
        # if k1.kick_count and k2.kick_count and ...:
        #     Issue.objects.create(...)

        # Turn / leap missing (Jazz)
        # if not k1.jazz_team_turn_performed and not k2.jazz_team_turn_performed:
        #     Issue.objects.create(...)

        # This file is the right place to encode those exact rules later.
        pass

    # Falls / dangerous moves → potential panel-majority issues
    falls_flag = any(k.falls_observed for k in kcts)
    dangerous_flag = any(k.dangerous_move_observed for k in kcts)

    if falls_flag:
        Issue.objects.create(
            team_entry=team_entry,
            issue_type=IssueType.FALL,
            severity=IssueSeverity.POTENTIAL_DEDUCTION,
            description="Fall observed by KCT.",
        )

    if dangerous_flag:
        Issue.objects.create(
            team_entry=team_entry,
            issue_type=IssueType.DANGEROUS_MOVE,
            severity=IssueSeverity.POTENTIAL_DEDUCTION,
            description="Dangerous move observed by KCT.",
        )


def create_judging_issues(team_entry):
    """
    Judge-based issues:
    - Missing sheets
    - Comment keywords (illegal, dangerous, fall, etc.)
    - Outliers (later, if you want)
    """
    sheets = list(JudgeScoreSheet.objects.filter(team_entry=team_entry))

    # Missing judge sheets (you can refine this once you have assignment logic)
    if not sheets:
        Issue.objects.create(
            team_entry=team_entry,
            issue_type=IssueType.OTHER,
            severity=IssueSeverity.WARNING,
            description="No judge score sheets submitted for this routine.",
        )

    # If you later add a comments field, scan it here:
    # for s in sheets:
    #     text = (s.comments or "").lower()
    #     if "illegal" in text:
    #         Issue.objects.create(...)
    #     if "dangerous" in text:
    #         Issue.objects.create(...)
    #     if "fall" in text:
    #         Issue.objects.create(...)


@transaction.atomic
def regenerate_issues_for_entry(team_entry):
    """
    Main entry point: clear auto issues and rebuild from KCT + Judging.
    Call this from signals.
    """
    _clear_auto_issues(team_entry)
    create_kct_issues(team_entry)
    create_judging_issues(team_entry)
