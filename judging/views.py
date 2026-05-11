from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from meets.models import TeamEntry
from judging.models import JudgeScoreSheet
from judging.scoring import ScoringEngine

from core.permissions import user_is_judge
    
#####  JUDGES VIEW  #####
@login_required
def judge_score_entry(request, team_entry_id):
    if not user_is_judge(request.user):
        messages.error(request, "You do not have permission to access this page.")
        return redirect("/")
    
    team_entry = get_object_or_404(TeamEntry, id=team_entry_id)
    
    # Get or create the Judges' Scoresheet
    sheet, created = JudgeScoreSheet.objects.get_or_create(
        team_entry=team_entry,
        judge=request.user,
        defaults={"judge_number": request.user.judge_number},
    )
    
    if request.method == "POST":
        # Update scoring categories
        sheet.performance = request.POST.get("performance")
        sheet.choreography = request.POST.get("choreography")
        sheet.execution = request.POST.get("execution")
        sheet.presentation = request.POST.get("presentation")
        sheet.comments = request.POST.get("comments", "")
        
        sheet.save()
        
        # Recompute Totals
        ScoringEngine.apply_to_scoresheet(sheet, user=request.user)
        
        messages.success(request, "Scores saved.")
        return redirect("judge_score_entry", team_entry_id=team_entry_id)
    
    return render(request, "judging/judge_score_entry.html", {
        "team_entry": team_entry,
        "sheet": sheet,
    })
    
