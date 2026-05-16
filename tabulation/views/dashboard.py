from django.shortcuts import render
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from superior.models import Issue
from deductions.models import RoutineDeduction
from collections import defaultdict

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

    # Add deductions to tabulation dashboard
    deductions = RoutineDeduction.objects.filter(
        team_entry__meet=meet
    ).select_related("team_entry", "deduction_type")

    summary = defaultdict(lambda: {"team": None, "total": 0, "items": []})

    for d in deductions:
        entry = d.team_entry
        summary[entry.id]["team"] = entry.team.name
        summary[entry.id]["total"] += d.total_points()
        summary[entry.id]["items"].append({
            "label": d.deduction_type.label,
            "points": d.total_points(),
            "count": d.count,
        })


    return render(request, "tabulation/dashboard.html", {
        "meet_data": meet_data, "deduction_summary": summary,
    })
