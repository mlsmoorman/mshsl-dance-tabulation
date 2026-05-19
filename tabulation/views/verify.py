from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from meets.models.entry import TeamEntry


@login_required
def tabulator_verify(request, meet_id):
    if not request.user.has_role("TABULATOR"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school", "kct_entry")
        .prefetch_related("issues", "score_sheets")
        .order_by("performance_order")
    )

    required_judges = meet.judges.count()

    verification = []
    for entry in entries:
        sheets = entry.score_sheets.all()
        unresolved = entry.issues.filter(resolved_at__isnull=True)
        kct = getattr(entry, "kctentry", None)
        dq = getattr(entry, "dq_entry", None)

        verification.append({
            "entry": entry,
            "judges_submitted": sheets.count(),
            "required_judges": required_judges,
            "missing_judge_sheets": sheets.count() < required_judges,
            "kct_missing": kct is None,
            "unresolved_issues": unresolved,
            "dq": dq,
        })

    return render(request, "tabulation/tabulator_verify.html", {
        "meet": meet,
        "verification": verification,
    })
