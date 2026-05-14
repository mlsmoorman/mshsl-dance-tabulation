from django.shortcuts import render, redirect, get_object_or_404
from core.models import Team
from meets.models.entry import TeamEntry
from meets.forms import TeamEntryForm

def add_entry(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        form = TeamEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.team = team
            entry.meet = team.meet
            entry.save()
            return redirect("meet_setup")
    else:
        form = TeamEntryForm()

    return render(request, "meets/add_entry.html", {
        "team": team,
        "form": form,
    })
