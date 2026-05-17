from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from ..models import Issue
from ..forms import IssueResolutionForm
from tabulation.models import MeetLock


def resolve_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    team_entry = issue.team_entry

    if MeetLock.objects.filter(meet=team_entry.meet).exists():
        return HttpResponseForbidden("Meet is locked.")


    if request.method == "POST":
        form = IssueResolutionForm(request.POST, instance=issue)
        if form.is_valid():
            action = form.cleaned_data["resolution_action"]
            notes = form.cleaned_data["resolution_notes"]
            issue.resolve(request.user, action, notes)
            return redirect("superior:review", entry_id=team_entry.id)
    else:
        form = IssueResolutionForm(instance=issue)

    return render(request, "superior/resolve_issue.html", {
        "form": form,
        "issue": issue,
        "team_entry": team_entry,
    })
