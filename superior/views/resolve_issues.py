from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from superior.models import Issue, IssueStatus
from django.http import HttpResponseForbidden
from deductions.models import DeductionType, RoutineDeduction
from tabulation.models import MeetLock

def resolve_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    if MeetLock.objects.filter(meet=issue.team_entry.meet).exists():
        return HttpResponseForbidden("Meet is locked.")


	# 1. Mark issue resolved
    if request.method == "POST":
        action = request.POST.get("action")
        notes = request.POST.get("notes", "")
        
		# Mark issue resolved
        issue.status = IssueStatus.RESOLVED
        issue.resolved_by = request.user
        issue.resolved_at = timezone.now()
        issue.resolution_action = action
        issue.resolution_notes = notes
        issue.save()
        
		# Auto-apply deduction
        if action == "APPLY_DEDUCTION":
            deduction_type = DeductionType.objects.get(code=issue.issue_type)
            
            RoutineDeduction.objects.create(
				team_entry=issue.team_entry,
				deduction_type=deduction_type,
				count=1,
				notes=f"Auto-applied from SJ resolution: {issue.description}",
                applied_by=request.user,
			)
            
			# Recompute all judge sheets
            for sheet in issue.team_entry.score_sheets.all():
                sheet.save()
                
        return redirect("superior:issues_dashboard", meet_id=issue.team_entry.meet.id)

    return render(request, "superior/resolve_issue.html", {
        "issue": issue,
    })
