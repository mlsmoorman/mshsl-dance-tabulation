from django.shortcuts import render, get_object_or_404, redirect
from superior.models import Issue, IssueType, IssueSeverity
from meets.models.entry import TeamEntry

def judge_flag_issue(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    if request.method == "POST":
        Issue.objects.create(
            team_entry=entry,
            created_by=request.user,
            issue_type=IssueType.OTHER,  # or whatever type you want judges to flag
            severity=IssueSeverity.WARNING,
            description=request.POST.get("description", ""),
        )
        return redirect("judging:judge_dashboard", meet_id=entry.meet.id)

    return render(request, "judging/judge_flag_issue.html", {
        "entry": entry,
    })
