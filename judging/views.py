from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from meets.models import Meet, TeamEntry, Division
from .models import JudgeScoreSheet
from .forms import JudgeScoreSheetForm



@login_required
def judge_meet_sheets(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    sheets = (
        JudgeScoreSheet.objects
        .filter(judge=request.user, team_entry__meet=meet)
        .select_related("team_entry__team", "team_entry__team__school")
    )

    return render(request, "judging/judge_meet_sheets.html", {
        "meet": meet,
        "sheets": sheets,
    })


@login_required
def edit_score_sheet(request, pk):
    sheet = get_object_or_404(JudgeScoreSheet, id=pk, judge=request.user)

    if request.method == "POST":
        form = JudgeScoreSheetForm(request.POST, instance=sheet)
        if form.is_valid():
            form.save()
            return redirect("judging:judge_meet_sheets", meet_id=sheet.team_entry.meet.id)
    else:
        form = JudgeScoreSheetForm(instance=sheet)

    return render(request, "judging/edit_score_sheet.html", {
        "sheet": sheet,
        "form": form,
    })



@login_required
def superior_review(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    entries = TeamEntry.objects.filter(meet=meet).select_related("team", "team__school")

    jazz = (
        entries.filter(division=Division.JAZZ)
        .annotate(total_score=Sum("score_sheets__total"))
        .order_by("-total_score")
    )

    kick = (
        entries.filter(division=Division.KICK)
        .annotate(total_score=Sum("score_sheets__total"))
        .order_by("-total_score")
    )

    return render(request, "judging/superior_review.html", {
        "meet": meet,
        "jazz_entries": jazz,
        "kick_entries": kick,
    })

