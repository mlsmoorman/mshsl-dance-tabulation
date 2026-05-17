from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from tabulation.models import FinalResult
from judging.models import JudgeScoreSheet


@login_required
def judge_recap(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)

    # Frozen final results for this division
    results = FinalResult.objects.filter(
        meet=meet,
        entry__division=division
    ).select_related("entry", "entry__team").order_by("final_rank")

    # All judge sheets for this division
    sheets = JudgeScoreSheet.objects.filter(
        team_entry__meet=meet,
        team_entry__division=division
    ).select_related("judge", "team_entry", "team_entry__team")

    # Group sheets by entry
    sheets_by_entry = {}
    judges = set()

    for sheet in sheets:
        entry_id = sheet.team_entry.id
        judges.add(sheet.judge.judge_number)  # assuming judge_number exists

        if entry_id not in sheets_by_entry:
            sheets_by_entry[entry_id] = {}

        sheets_by_entry[entry_id][sheet.judge.judge_number] = {
            "total": sheet.total,
            "rank": sheet.rank,
        }

    judges = sorted(judges)

    # Build rows for template
    rows = []
    for r in results:
        entry_id = r.entry.id
        judge_data = sheets_by_entry.get(entry_id, {})

        rows.append({
            "entry": r.entry,
            "placement": r.final_placement,
            "total_score": r.final_total_score,
            "rank_points": {j: judge_data.get(j, {}).get("rank") for j in judges},
            "judge_totals": {j: judge_data.get(j, {}).get("total") for j in judges},
            "total_rank_points": r.final_rank_points,
        })

    return render(request, "tabulation/judge_recap.html", {
