from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from ..models import KCTEntry


def kct_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    # Group by division, sorted by performance order
    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team")
        .order_by("division", "performance_order")
    )

    # Build structure: {division: [entries]}
    divisions = {}
    for entry in entries:
        divisions.setdefault(entry.division, []).append(entry)

    # For each entry, attach KCT #1 and KCT #2 entries
    for entry in entries:
        entry.kct_entries_list = list(entry.kct_entries.all())

    return render(request, "kct/dashboard.html", {
        "meet": meet,
        "divisions": divisions,
        "user": request.user,
    })
