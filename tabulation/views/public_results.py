from django.shortcuts import render, get_object_or_404
from tabulation.models import FinalResult
from meets.models.meet import Meet

def public_results(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    results = FinalResult.objects.filter(meet=meet).order_by("final_rank")

    # Group by division for cleaner display
    divisions = {}
    for r in results:
        div = r.entry.division
        divisions.setdefault(div, []).append(r)

    return render(request, "tabulation/public_results.html", {
        "meet": meet,
        "divisions": divisions,
    })
