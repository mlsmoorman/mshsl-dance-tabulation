from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from meets.models import Meet, TeamEntry, Division
from .models import JudgeScoreSheet
from .forms import JudgeScoreSheetForm


# Judge Meet Sheets
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

# Edit Score Sheet
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


# Superior Review
@login_required
def superior_judge_review(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    # Only superior judges allowed
    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school")
    )

    # Build data rows
    data = []
    for entry in entries:
        total = (
            entry.score_sheets.aggregate(total=Sum("total")).get("total") or 0
        )

        data.append({
            "entry": entry,
            "team": entry.team,
            "school": entry.team.school,
            "division": entry.division,
            "order": entry.performance_order,
            "total": total,
        })

    # Split by division
    jazz = [d for d in data if d["division"] == Division.JAZZ]
    kick = [d for d in data if d["division"] == Division.KICK]

    # Sort by total descending
    jazz.sort(key=lambda d: d["total"], reverse=True)
    kick.sort(key=lambda d: d["total"], reverse=True)

    return render(request, "judging/superior_judge_review.html", {
        "meet": meet,
        "jazz_entries": jazz,
        "kick_entries": kick,
    })

