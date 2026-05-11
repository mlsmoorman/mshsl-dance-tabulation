from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from meets.models import TeamEntry
from judging.models import JudgeScoreSheet
from kct.models import KCTEntry
from deductions.models import RoutineDeduction
from meets.models import Meet, TeamEntry
from judging.models import JudgeScoreSheet
from judging.helpers import get_possible_issues

from core.permissions import user_is_tabulator

#####  TABULATOR VIEW  #####
@login_required
def tabulator_verify(request, team_entry_id):
    issues = get_possible_issues()
    
    if not user_is_tabulator(request.user):
        if user_is_superuser(request.user):
            return True,
        else: 
            messages.error(request, "You do not have permission to access this page.")
        return redirect("/")

    team_entry = get_object_or_404(TeamEntry, id=team_entry_id)
    kct = KCTEntry.objects.filter(team_entry=team_entry).order_by("-id").first()
    judge_sheets = JudgeScoreSheet.objects.filter(team_entry=team_entry)
    
    # All deductions (auto + manual)
    deductions = RoutineDeduction.objects.filter(team_entry=team_entry).order_by(
        "deduction_type__penalty_type", "deduction_type__code"
    )
    
    # Compute Totals
    subtotal_by_judge = {sheet.judge_number: sheet.compute_subtotal() for sheet in judge_sheets}
    deduction_total_by_judge = {sheet.judge_number: sheet.other_deduction for sheet in judge_sheets}
    total_by_judge = {sheet.judge_number: sheet.total_score for sheet in judge_sheets}
    
    if request.method == "POST":
        team_entry.verified_by_tabulator = True
        team_entry.save()
        messages.success(request, "Routine verified and locked.")
        return redirect("tabulator_verify", team_entry_id=team_entry_id)
    
    return render(request, "tabulation/tabulator_verify.html", {
        "team_entry": team_entry,
        "kct": kct,
        "judge_sheets": judge_sheets,
        "deductions": deductions,
        "subtotal_by_judge": subtotal_by_judge,
        "deduction_total_by_judge": deduction_total_by_judge,
        "total_by_judge": total_by_judge,
        "issues": issues,
    })


def tabulator_dashboard(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)
    entries = TeamEntry.objects.filter(meet=meet, division=division).order_by("performance_order")
    
    judges = meet.judges.all() if hasattr(meet, "judges") else []
    
    judge_status = []
    for judge in judges:
        total = entries.count()
        submitted = JudgeScoreSheet.objects.filter(team_entry__in=entries, judge=judge).count()
        missing = total - submitted
        judge_status.append({
            "judge": judge,
            "submitted": submitted,
            "missing": missing,
            "complete": missing == 0,
        })
    
    finalists = entries.filter(is_finalist=True).order_by("prelim_rank")
    finals_done = entries.filter(final_rank__isnull=False).exists()
    
    context = {
        "meet": meet,
        "division": division,
        "entries": entries,
        "judge_status": judge_status,
        "finalists": finalists,
        "finals_done": finals_done,
    }
    return render(request, "tabulation/tabulator_dashboard.html", context)