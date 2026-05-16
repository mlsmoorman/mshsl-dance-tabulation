from django.shortcuts import render, get_object_or_404, redirect
from superior.models import Issue, IssueStatus
from django.utils import timezone
from tabulation.models import DeductionType
from models import RoutineDeduction

def resolve_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

	# 1. Mark issue resolved
    if request.method == "POST":
        action = request.POST.get("action")
        notes = request.POST.get("notes", "")

        issue.status = IssueStatus.RESOLVED
        issue.resolved_by = request.user
        issue.resolved_at = timezone.now()
        issue.resolution_action = action
        issue.resolution_notes = notes
        issue.save()
    
    # 2. If SJ selected APPLY_DEDUCTION, create a deduction
    if action == "APPLY_DEDUCTION":
        # Map IssueType → DeductionType
        deduction_type = DeductionType.objects.get(code=issue.issue_type)
        
        RoutineDeduction.objects.create(
			team_entry=issue.team_entry,
			deduction_type=deduction_type,
			count=1,
			notes=f"Auto-applied from SJ issue resolution: {issue.description}",
		)
        
        # 3. Recompute all judge score sheets for this entry
        for sheet in issue.team_entry.score_sheets.all():
            sheet.save()  # triggers compute_total()

        return redirect("superior:issues_dashboard", meet_id=issue.team_entry.meet.id)

    return render(request, "superior/resolve_issue.html", {
        "issue": issue,
    })
