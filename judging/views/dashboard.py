from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from ..models import JudgeScoreSheet


def judge_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    # Routines assigned to this judge: for now, assume all entries in the meet
    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team")
        .order_by("division", "performance_order")
    )

    # Attach existing score sheet (if any) for this judge
    for entry in entries:
        entry.score_sheet = (
            JudgeScoreSheet.objects
            .filter(team_entry=entry, judge=request.user)
            .first()
        )

    return render(request, "judging/dashboard.html", {
        "meet": meet,
        "entries": entries,
    })
