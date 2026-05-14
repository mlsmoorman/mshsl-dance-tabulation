from django.shortcuts import render, redirect
from core.models import Team
from meets.forms import TeamForm

def add_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("meet_setup")
    else:
        form = TeamForm()

    return render(request, "meets/add_team.html", {
        "form": form,
    })
