from django.shortcuts import get_object_or_404, redirect
from deductions.models import RoutineDeduction
from judging.models import JudgeScoreSheet

def remove_deduction(request, deduction_id):
    deduction = get_object_or_404(RoutineDeduction, id=deduction_id)
    team_entry = deduction.team_entry
    meet_id = team_entry.meet.id

    # Delete the deduction
    deduction.delete()

    # Recompute all judge sheets for this team
    for sheet in team_entry.score_sheets.all():
        sheet.save()

    return redirect("superior:issues_dashboard", meet_id=meet_id)
