from django.shortcuts import render, get_object_or_404
from tabulation.models import FinalResult
from meets.models.meet import Meet

def meet_results(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)
    results = FinalResult.objects.filter(meet=meet).order_by("final_rank")

    return render(request, "tabulation/meet_results.html", {
        "meet": meet,
        "results": results,
    })

def tabulation_results(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    results = FinalResult.objects.filter(meet=meet).select_related(
        "entry", "entry__team"
    ).order_by("final_rank")

    return render(request, "tabulation/results.html", {
        "meet": meet,
        "results": results,
    })
