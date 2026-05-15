from django.shortcuts import render, get_object_or_404, redirect
from superior.models import Issue, IssueStatus
from django.utils import timezone

def resolve_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == "POST":
        action = request.POST.get("action")
        notes = request.POST.get("notes", "")

        issue.status = IssueStatus.RESOLVED
        issue.resolved_by = request.user
        issue.resolved_at = timezone.now()
        issue.resolution_action = action
        issue.resolution_notes = notes
        issue.save()

        return redirect("superior:issues_dashboard", meet_id=issue.team_entry.meet.id)

    return render(request, "superior/resolve_issue.html", {
        "issue": issue,
    })
