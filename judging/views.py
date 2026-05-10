from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from meets.models import TeamEntry
from judging.models import JudgeScoreSheet, KCTEntry
from deductions.models import DeductionType, RoutineDeduction
from core.models import Role
from judging.scoring import ScoringEngine


#####  SUPERIOR JUDGE VIEW  #####
def user_is_superior_judge(user):
    return user.roles.filter(name="Superior Judge").exists()
    
@login_required
def superior_judge_review(request, team_entry_id):
    if not user_is_superior_judge(request.user):
        messages.error(request, "You do not have permission to access this page.")
        return redirect("/")

    team_entry = get_object_or_404(TeamEntry, id=team_entry_id)
    kct = KCTEntry.objects.filter(team_entry=team_entry).order_by("-id").first()
    judge_sheets = JudgeScoreSheet.objects.filter(team_entry=team_entry)

    # Auto-applied deductions (read-only)
    auto_deductions = RoutineDeduction.objects.filter(
        team_entry=team_entry,
        deduction_type__code__in=["TIME_REQUIREMENTS", "KICK_REQUIREMENTS"]
    )

    # Manual deductions (Superior Judge entered)
    manual_deductions = RoutineDeduction.objects.filter(
        team_entry=team_entry
    ).exclude(
        deduction_type__code__in=["TIME_REQUIREMENTS", "KICK_REQUIREMENTS"]
    )

    # Deduction types available for manual entry
    deduction_types = DeductionType.objects.exclude(
        code__in=["TIME_REQUIREMENTS", "KICK_REQUIREMENTS"]
    ).order_by("penalty_type", "code")

    if request.method == "POST":
        deduction_type_id = request.POST.get("deduction_type")
        notes = request.POST.get("notes", "")
        count = int(request.POST.get("count", 1))

        dt = get_object_or_404(DeductionType, id=deduction_type_id)

        RoutineDeduction.objects.create(
            team_entry=team_entry,
            deduction_type=dt,
            entered_by=request.user,
            count=count,
            judges_reporting=1,
            notes=notes,
        )

        messages.success(request, f"{dt.code} deduction added.")
        return redirect("superior_judge_review", team_entry_id=team_entry.id)

    return render(request, "judging/superior_judge_review.html", {
        "team_entry": team_entry,
        "kct": kct,
        "judge_sheets": judge_sheets,
        "auto_deductions": auto_deductions,
        "manual_deductions": manual_deductions,
        "deduction_types": deduction_types,
    })

#####  TABULATOR VIEW  #####
def user_is_tabulator(user):
    return user.roles.filter(name="Tabulator").exists()

@login_required
def tabulator_verify(request, team_entry_id):
    if not user_is_tabulator(request.user):
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
    
    return render(request, "judging/tabulator_verify.html", {
        "team_entry": team_entry,
        "kct": kct,
        "judge_sheets": judge_sheets,
        "deductions": deductions,
        "subtotal_by_judge": subtotal_by_judge,
        "deduction_total_by_judge": deduction_total_by_judge,
        "total_by_judge": total_by_judge,
    })
    
#####  JUDGES VIEW  #####
def user_is_judge(user):
    return user.roles.filter(name="Judge").exists()

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