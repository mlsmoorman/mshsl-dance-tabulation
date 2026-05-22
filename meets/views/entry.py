from django.shortcuts import render, redirect, get_object_or_404
from core.models import Team
from meets.models.meet import Meet
from meets.forms import TeamEntryForm

def add_entry(request, meet_id, team_id):
    meet = get_object_or_404(Meet, id=meet_id)
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        form = TeamEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.meet = meet
            entry.team = team
            entry.save()
            return redirect("meet_setup")
    else:
        form = TeamEntryForm()

    return render(request, "meets/add_entry.html", {
        "meet": meet,
        "team": team,
        "form": form,
    })

