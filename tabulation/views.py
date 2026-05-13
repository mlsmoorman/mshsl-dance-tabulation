from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone   

from meets.models import TeamEntry
from judging.models import JudgeScoreSheet
from kct.models import KCTEntry
from deductions.models import RoutineDeduction
from meets.models import Meet, TeamEntry
from judging.models import JudgeScoreSheet
from judging.helpers import get_possible_issues

from core.permissions import user_is_tabulator


#~.~.~.~.~.~.~.~.~.~.~.~.~ TABULATOR VERIFY ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def tabulator_verify(request, meet_id):
    if not request.user.has_role("TABULATOR"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school", "kctentry")
        .prefetch_related("score_sheets", "issues")
        .order_by("performance_order")
    )

    # Build verification data
    verification = []

    for entry in entries:
        sheets = entry.score_sheets.all()
        judges_submitted = sheets.count()
        required_judges = meet.judges.count()

        unresolved_issues = entry.issues.filter(resolved=False)

        kct = getattr(entry, "kctentry", None)

        verification.append({
            "entry": entry,
            "judges_submitted": judges_submitted,
            "required_judges": required_judges,
            "missing_judge_sheets": judges_submitted < required_judges,
            "kct_missing": kct is None,
            "unresolved_issues": unresolved_issues,
            "dq": entry.disqualified,
        })

    return render(request, "tabulation/tabulator_verify.html", {
        "meet": meet,
        "verification": verification,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~ TABULATOR DASHBOARD ~.~.~.~.~.~.~.~.~.~.~.~.~#
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


#~.~.~.~.~.~.~.~.~.~.~.~.~ LOCK MEET ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def lock_meet(request, meet_id):
    if not request.user.has_role("TABULATOR"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)
    meet.locked = True
    meet.locked_at = timezone.now()
    meet.locked_by = request.user
    meet.save()

    return redirect("tabulation:final_results", meet_id=meet.id)


#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#