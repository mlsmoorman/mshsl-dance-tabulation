from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from superior.models import Issue, IssueType, IssueSeverity
from meets.models.entry import TeamEntry
from tabulation.models import MeetLock

def judge_flag_issue(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    if MeetLock.objects.filter(meet=entry.meet).exists():
        return HttpResponseForbidden("Meet is locked.")

    
    if request.method == "POST":
        Issue.objects.create(
            team_entry=entry,
            created_by=request.user,
            issue_type=request.POST.get("issue_type"),
            severity=IssueSeverity.WARNING,
            description=request.POST.get("description", ""),
        )
        return redirect("judging:judge_dashboard", meet_id=entry.meet.id)

    return render(request, "judging/judge_flag_issue.html", {
        "entry": entry,
        "issue_types": IssueType.choices,
    })
