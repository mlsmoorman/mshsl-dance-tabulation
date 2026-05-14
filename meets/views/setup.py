from django.shortcuts import render, redirect
from meets.models.meet import Meet
from core.models import Team
from meets.models.entry import TeamEntry
from meets.forms import MeetForm

def meet_setup(request):
    meets = Meet.objects.all().order_by("-date")

    if request.method == "POST":
        form = MeetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("meet_setup")
    else:
        form = MeetForm()

    # Build nested structure: Meet → Teams → Entries
    meet_data = []
    for meet in meets:
        teams = Team.objects.filter(school__isnull=False)  # all teams, or filter later
        team_entries = {
            team.id: TeamEntry.objects.filter(team=team, meet=meet)
            for team in teams
        }

        meet_data.append({
            "meet": meet,
            "teams": teams,
            "entries": team_entries,
        })

    return render(request, "meets/meet_setup.html", {
        "form": form,
        "meet_data": meet_data,
    })


