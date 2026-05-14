from django.shortcuts import render
from meets.models.meet import Meet
from superior.models import Issue

def tabulator_dashboard(request):
    meets = Meet.objects.all().order_by("-date")

    meet_data = []
    for meet in meets:
        entries = meet.teamentry_set.all()
        unresolved_issues = Issue.objects.filter(
            team_entry__in=entries,
            resolved=False
        ).count()

        meet_data.append({
            "meet": meet,
            "entries_count": entries.count(),
            "unresolved_issues": unresolved_issues,
            "is_locked": meet.locked,
        })

    return render(request, "tabulation/tabulator_dashboard.html", {
        "meet_data": meet_data,
    })
