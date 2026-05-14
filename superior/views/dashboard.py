from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models.entry import TeamEntry


def superior_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team")
        .order_by("division", "performance_order")
    )

    for entry in entries:
        entry.open_issues = entry.issues.filter(status="OPEN")
        entry.dq = entry.dq_entries.filter(status__in=["PENDING", "CONFIRMED"]).first()

    return render(request, "superior/dashboard.html", {
        "meet": meet,
        "entries": entries,
    })
