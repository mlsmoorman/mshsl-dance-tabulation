from django.shortcuts import render, get_object_or_404, redirect
from superior.models import Issue, IssueStatus
from meets.models import Meet
from deductions.models import RoutineDeduction
from collections import defaultdict

def superior_issues_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    issues = Issue.objects.filter(
        team_entry__meet=meet,
        status=IssueStatus.OPEN
    ).select_related(
        "team_entry", "created_by"
    ).order_by(
        "team_entry__performance_order",
        "-created_at"
    )
    
    # Group issues by team entry
    issues_by_team = defaultdict(list)

    for issue in issues:
        issues_by_team[issue.team_entry].append(issue)

    # Prefetch deductions for all team entries in this meet
    deductions = RoutineDeduction.objects.filter(
        team_entry__meet=meet
    ).select_related("deduction_type", "team_entry")


    # Build a summary: { team_entry_id: { "team": name, "total": X, "items": [...] } }
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

    
    return render(request, "superior/issues_dashboard.html", {
        "meet": meet,
        "issues": issues,
        "deductions": deductions,
        "deduction_summary": summary,
        "issues_by_team": issues_by_team,
    })
    
    
