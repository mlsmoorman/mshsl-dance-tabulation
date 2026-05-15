from django.shortcuts import render, get_object_or_404
from judging.models.judge_score_sheet import JudgeScoreSheet
from meets.models.entry import TeamEntry

def view_score_sheets(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    sheets = (
        JudgeScoreSheet.objects
        .filter(team_entry=entry)
        .select_related("judge")
        .order_by("-total")
    )

    return render(request, "judging/view_score_sheet.html", {
        "entry": entry,
        "sheets": sheets,
        "compare": request.GET.get("compare") == "1",
    })
