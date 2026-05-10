from django.shortcuts import render, get_object_or_404
from meets.ranking import compute_rankings

# Create your views here.
def meet_summary(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    jazz_rankings = compute_rankings(meet, "JAZZ")
    kick_rankings = compute_rankings(meet, "KICK")

    return render(request, "meets/summary.html", {
        "meet": meet,
        "jazz_rankings": jazz_rankings,
        "kick_rankings": kick_rankings,
    })