from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models import TeamEntry

def kct_division_selector(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    divisions = (
        TeamEntry.objects
        .filter(meet=meet)
        .values_list("division", flat=True)
        .distinct()
    )

    return render(request, "kct/division_selector.html", {
        "meet": meet,
        "divisions": divisions,
    })
