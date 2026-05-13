from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from meets.models.entry import TeamEntry, Division


@login_required
def announcer_results(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    divisions = {}
    for division in Division.values:
        entries = (
            TeamEntry.objects
            .filter(meet=meet, division=division, final_placement__isnull=False)
            .order_by("final_placement")
        )
        if entries.exists():
            divisions[division] = entries

    return render(request, "tabulation/announcer_results.html", {
        "meet": meet,
        "divisions": divisions,
    })
