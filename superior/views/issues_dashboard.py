from django.shortcuts import render, get_object_or_404, redirect
from superior.models import Issue, IssueStatus
from meets.models import Meet
from deductions.models import RoutineDeduction


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

    # Prefetch deductions for all team entries in this meet
    deductions = RoutineDeduction.objects.filter(
        team_entry__meet=meet
    ).select_related("deduction_type", "team_entry")

    return render(request, "superior/issues_dashboard.html", {
        "meet": meet,
        "issues": issues,
        "deductions": deductions,
    })
