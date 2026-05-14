from django.shortcuts import redirect
from meets.forms import InlineTeamForm

def add_team_inline(request, meet_id):
    if request.method == "POST":
        form = InlineTeamForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("meet_overview", meet_id=meet_id)
