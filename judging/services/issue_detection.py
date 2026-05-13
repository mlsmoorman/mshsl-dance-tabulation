from judging.models import Issue, IssueType
import statistics

from judging.models import Division


#~.~.~.~.~.~.~.~.~.~.~.~.~ DETECT TIMING VIOLATION ~.~.~.~.~.~.~.~.~.~.~.~.~#
def detect_timing_violation(entry):
    kct = getattr(entry, "kctentry", None)
    if not kct or not kct.actual_time_seconds:
        return

    # Jazz: 1:30–2:00
    # Kick: 2:15–2:45
    if entry.division == Division.JAZZ:
        min_time = 90
        max_time = 120
    else:  # Kick
        min_time = 135
        max_time = 165

    if kct.actual_time_seconds < min_time or kct.actual_time_seconds > max_time:
        Issue.objects.get_or_create(
            team_entry=entry,
            issue_type=IssueType.TIME,
            auto_generated=True,
            defaults={
                "message": (
                    f"Routine time {kct.actual_time_seconds}s is outside allowed "
                    f"range ({min_time}–{max_time} seconds) for {entry.division}."
                )
            }
        )


#~.~.~.~.~.~.~.~.~.~.~.~.~ DETECT KICK COUNT VIOLATION ~.~.~.~.~.~.~.~.~.~.~.~.~#        
def detect_kick_violation(entry):
    kct = getattr(entry, "kctentry", None)
    if not kct or not kct.kick_count:
        return
    
    min_kicks = 35  # 1:30  ~ Can be updated if rules change
    max_kicks = 55  # 2:00  ~ Can be updated if rules change
    
    if kct.kick_count < min_kicks or kct.kick_count > max_kicks:
        Issue.objects.get_or_create(
			team_entry=entry,
			issue_type=IssueType.KICK,
			auto_generated=True,
			defaults=(
				"message": f"Kick count {kct.kick_count} is outside allowed range."
			)
		)
        
        
#~.~.~.~.~.~.~.~.~.~.~.~.~ DETECT MISSING SCORESHEET ~.~.~.~.~.~.~.~.~.~.~.~.~#
def detect_missing_sheets(entry):
    meet_judges = entry.meet.judges.all()
    submitted = entry.score_sheets.values_list("judge_id", flat=True)

    for judge in meet_judges:
        if judge.id not in submitted:
            Issue.objects.get_or_create(
                team_entry=entry,
                issue_type=IssueType.MISSING_SHEET,
                auto_generated=True,
                defaults={
                    "message": f"Judge {judge.username} did not submit a score sheet."
                }
            )


#~.~.~.~.~.~.~.~.~.~.~.~.~ DETECT SCORE OUTLIERS ~.~.~.~.~.~.~.~.~.~.~.~.~#
def detect_score_outliers(entry):
    sheets = entry.score_sheets.all()
    totals = [float(s.total) for s in sheets]

    if len(totals) < 3:
        return  # not enough data

    median = statistics.median(totals)

    for sheet in sheets:
        if sheet.total > median * 1.20 or sheet.total < median * 0.80:
            Issue.objects.get_or_create(
                team_entry=entry,
                issue_type=IssueType.SCORE_OUTLIER,
                auto_generated=True,
                defaults={
                    "message": (
                        f"Judge {sheet.judge.username} score {sheet.total} "
                        f"deviates significantly from median {median}."
                    )
                }
            )


#~.~.~.~.~.~.~.~.~.~.~.~.~ DETECT COMPETITOR VIOLATION ~.~.~.~.~.~.~.~.~.~.~.~.~#
def detect_competitor_violation(entry):
    # Only applies to Varsity
    if entry.team.level != "Varsity":
        return

    if entry.competitor_count is None:
        return

    min_comp = 5

    # Division-specific maximums
    if entry.division == Division.JAZZ:
        max_comp = 26
    else:  # Kick
        max_comp = 34

    if entry.competitor_count < min_comp or entry.competitor_count > max_comp:
        Issue.objects.get_or_create(
            team_entry=entry,
            issue_type=IssueType.COMPETITOR,
            auto_generated=True,
            defaults={
                "message": (
                    f"Competitor count {entry.competitor_count} is outside allowed "
                    f"range ({min_comp}–{max_comp}) for {entry.division} Varsity."
                )
            }
        )


#~.~.~.~.~.~.~.~.~.~.~.~.~ RUN ALL ISSUES AUTOMATICALLY ~.~.~.~.~.~.~.~.~.~.~.~.~#
def run_all_issue_detectors(entry):
    detect_timing_violation(entry)
    detect_kick_violation(entry)
    detect_missing_sheets(entry)
    detect_score_outliers(entry)
    detect_competitor_violation(entry)


