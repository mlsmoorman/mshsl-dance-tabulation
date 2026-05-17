from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from deductions.models import RoutineDeduction
from judging.models import JudgeScoreSheet
from django.utils import timezone
from tabulation.models import MeetLock

def remove_deduction(request, deduction_id):
    deduction = get_object_or_404(RoutineDeduction, id=deduction_id)
    team_entry = deduction.team_entry
    meet_id = team_entry.meet.id
    
    if MeetLock.objects.filter(meet=team_entry.meet).exists():
        return HttpResponseForbidden("Meet is locked.")
    
    # Delete the deduction
    deduction.removed_by = request.user
    deduction.removed_at = timezone.now()
    deduction.save()
    deduction.delete()
    

    # Recompute all judge sheets for this team
    for sheet in team_entry.score_sheets.all():
        sheet.save()

    return redirect("superior:issues_dashboard", meet_id=meet_id)
