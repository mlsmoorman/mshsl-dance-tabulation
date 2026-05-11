from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from meets.ranking import compute_rankings, advance_to_finals
from meets.models import Meet
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