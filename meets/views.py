from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from core.models import Team
from .models import Division
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from meets.forms import TeamEntryForm


#***********************************************************************CHANGES BEGIN:

#~.~.~.~.~.~.~.~.~.~.~.~.~ MEET SETUP VIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def meet_setup(request, meet_id=None):
    # create/edit meet, add entries, assign judges, etc.
    ...



#***********************************************************************CHANGES END.


#~.~.~.~.~.~.~.~.~.~.~.~.~ TABULATOR DASHBOARD ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def tabulator_dashboard(request, pk):
    # Only tabulators can access this page
    if not request.user.has_role("TABULATOR"):
        return redirect("/")  # or a 403 page

    meet = get_object_or_404(Meet, id=pk)

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school")
    )

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
            "verified": entry.verified_by_tabulator,
            "total": total,
        })

    jazz = [d for d in data if d["division"] == Division.JAZZ]
    kick = [d for d in data if d["division"] == Division.KICK]

    jazz.sort(key=lambda d: d["total"], reverse=True)
    kick.sort(key=lambda d: d["total"], reverse=True)

    return render(request, "meets/tabulator_dashboard.html", {
        "meet": meet,
        "jazz_entries": jazz,
        "kick_entries": kick,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~ VERIFY ENTRY ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def verify_entry(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    entry.verified_by_tabulator = True
    entry.save()
    return redirect(request, "meets:tabulator_dashboard", pk=entry.meet.id)


#~.~.~.~.~.~.~.~.~.~.~.~.~ FINALIZE MEET ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def finalize_meet(request, pk):
    meet = get_object_or_404(Meet, id=pk)
    entries = TeamEntry.objects.filter(meet=meet)
    
    entries = entries.filter(disqualified=False)
    
    # Compute Totals
    scored = []
    for entry in entries:
        total = (
            entry.score_sheets.aggregate(total=Sum("total")).get("total") or 0
        )
        scored.append((entry, total))
        
    # Split by Division
    jazz = [x for x in scored if x[0].division == Division.JAZZ]
    kick = [x for x in scored if x[0].division == Division.KICK]
    
    # Sort Descending
    jazz.sort(key=lambda x: x[1], reverse=True)
    kick.sort(key=lambda x: x[1], reverse=True)
    
    # Assign Ranks
    for rank, (entry, total) in enumerate(jazz, start=1):
        entry.final_rank = rank
        entry.save()
    
    for rank, (entry, total) in enumerate(kick, start=1):
        entry.final_rank = rank
        entry.save()
    
    return redirect(request, "meets.tabulator_dashboard", pk=pk)


#~.~.~.~.~.~.~.~.~.~.~.~.~ SELECT FINALISTS ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def select_finalists(request, pk):
    meet = get_object_or_404(Meet, id=pk)
    finalists = meet.num_finalists
    
    entries = TeamEntry.objects.filter(meet=meet).order_by("final_rank")
    
    # Reset All
    entries.update(is_finalist=False)
    
    # Select Finalists per Division
    for division in [Division.JAZZ, Division.KICK]:
        division_entries = entries.filter(division=division).order_by("final_rank")
        for entry in division_entries[:finalists]:
            entry.is_finalist = True
            entry.save()
            
    return redirect(request, "meets:tabulator_dashboard", pk=pk)




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

