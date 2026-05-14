from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from superior.models import Issue

def meet_overview(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    entries = TeamEntry.objects.filter(meet=meet, is_active=True)

    issues = Issue.objects.filter(
        team_entry__in=entries,
        resolved_at__isnull=True
    )

    # Group entries by division
    divisions = {}
    for entry in entries:
        divisions.setdefault(entry.division, []).append(entry)



    return render(request, "tabulation/meet_overview.html", {
        "meet": meet,
        "divisions": divisions,
        "issues": issues,
    })
