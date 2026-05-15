from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models.entry import TeamEntry

def kct_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    entries = (
        TeamEntry.objects
        .filter(meet=meet, is_active=True)
        .order_by("division", "performance_order")
    )

    return render(request, "kct/dashboard.html", {
        "meet": meet,
        "entries": entries,
    })

