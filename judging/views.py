from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from meets.models import TeamEntry
from judging.models import JudgeScoreSheet, KCTEntry
from deductions.models import DeductionType, RoutineDeduction
from core.models import Role


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
