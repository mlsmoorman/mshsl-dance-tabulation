from django.shortcuts import render
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from superior.models import Issue

def tabulator_dashboard(request):
    meets = Meet.objects.all().order_by("-date")

    meet_data = []

    for meet in meets:
        entries = TeamEntry.objects.filter(meet=meet)

        unresolved_issues = Issue.objects.filter(
            team_entry__in=entries,
            resolved_at__isnull=True
        )

        meet_data.append({
            "meet": meet,
            "entries": entries,
            "unresolved_count": unresolved_issues.count(),
        })

    return render(request, "tabulation/dashboard.html", {
        "meet_data": meet_data,
    })
