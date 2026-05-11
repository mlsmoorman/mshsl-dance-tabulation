from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from meets.ranking import compute_rankings, advance_to_finals
from meets.models import Meet, TeamEntry
from meets.ranking import compute_rankings
from core.permissions import user_is_tabulator


def meet_summary(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    jazz_rankings = compute_rankings(meet, "JAZZ")
    kick_rankings = compute_rankings(meet, "KICK")

    return render(request, "meets/summary.html", {
        "meet": meet,
        "jazz_rankings": jazz_rankings,
        "kick_rankings": kick_rankings,
    })
    
@login_required
def advance_to_finals_view(request, meet_id, division):
    if not user_is_tabulator(request.user):
        messages.error(request, "You do not have permission.")
        return redirect("/")
    
    meet = get_object_or_404(Meet, id=meet_id)
    finalists = advance_to_finals(meet, division)
    
    messages.success(request, f"{len(finalists)} teams advance to finals for {division}.")
    return redirect("meet_summary", meet_id=meet.id)


def run_prelims_ranking(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)
    entries = TeamEntry.objects.filter(meet=meet, division=division)
    
    results = compute_rankings(entries)
    
    for i in enumerate(results, start=1):
        entry = results["entry"]
        entry.prelim_rank = i
        entry.save()
        
    messages.success(request, f"Prelims ranking completed for {division}.")
    return redirect("tabular_dashboard", meet_id=meet_id, division=division)

def advance_finalists(request, meet_id, division):
    meet = get_object_or_404(Meet, meet_id)
    entries = TeamEntry.objects.filter(meet=meet, division=division).order_by("prelim_rank")
    
    finalists = entries[: meet.num_finalists]
    
    for entry in finalists:
        entry.is_finalist = True
        entry.save()
        
    messages.success(request, f"Finalists selected for {division}")
    return redirect("tabular_dashboard", meet_id=meet_id, division=division)

def run_finals_ranking(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)
    finalists = TeamEntry.objects.filter(meet=meet, division=division, is_finalist=True)

    results = compute_rankings(finalists)

    for i, result in enumerate(results, start=1):
        entry = result["entry"]
        entry.final_rank = i
        entry.placement = i
        entry.save()

    messages.success(request, f"Finals ranking completed for {division}.")
    return redirect("tabulator_dashboard", meet_id=meet.id, division=division)
    