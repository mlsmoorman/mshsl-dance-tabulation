from django.shortcuts import render, get_object_or_404
from meets.models.entry import TeamEntry
from kct.models import KCTEntry
from judging.models import JudgeScoreSheet


def superior_review(request, entry_id):
    team_entry = get_object_or_404(TeamEntry, id=entry_id)

    kct_entries = list(
        KCTEntry.objects.filter(team_entry=team_entry).select_related("kct")
    )
    judge_sheets = list(
        JudgeScoreSheet.objects.filter(team_entry=team_entry).select_related("judge")
    )
    issues = team_entry.issues.all().order_by("status", "-created_at")
    dq_entries = team_entry.dq_entries.all().order_by("-created_at")

    return render(request, "superior/review.html", {
        "team_entry": team_entry,
        "kct_entries": kct_entries,
        "judge_sheets": judge_sheets,
        "issues": issues,
        "dq_entries": dq_entries,
    })
