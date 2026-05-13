from django.shortcuts import render, redirect, get_object_or_404
from ..models import JudgeScoreSheet
from ..forms import JudgeScoreSheetForm
from meets.models.entry import TeamEntry


def judge_score_sheet(request, entry_id):
    team_entry = get_object_or_404(TeamEntry, id=entry_id)

    score_sheet, created = JudgeScoreSheet.objects.get_or_create(
        team_entry=team_entry,
        judge=request.user,
    )

    if request.method == "POST":
        form = JudgeScoreSheetForm(
            request.POST,
            instance=score_sheet,
            team_entry=team_entry,
        )
        if form.is_valid():
            form.save()
            return redirect("judging:dashboard", meet_id=team_entry.meet.id)
    else:
        form = JudgeScoreSheetForm(
            instance=score_sheet,
            team_entry=team_entry,
        )

    return render(request, "judging/score_sheet.html", {
        "form": form,
        "team_entry": team_entry,
    })
