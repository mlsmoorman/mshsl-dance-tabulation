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
        .select_related("team", "team__school", "kctentry")
        .prefetch_related("issues", "judgesscoresheet_set")
        .order_by("performance_order")
    )

    required_judges = meet.judges.count()

    verification = []
    for entry in entries:
        sheets = entry.judgesscoresheet_set.all()
        unresolved = entry.issues.filter(resolved=False)
        kct = getattr(entry, "kctentry", None)

        verification.append({
            "entry": entry,
            "judges_submitted": sheets.count(),
            "required_judges": required_judges,
            "missing_judge_sheets": sheets.count() < required_judges,
            "kct_missing": kct is None,
            "unresolved_issues": unresolved,
            "dq": entry.disqualified,
        })

    return render(request, "tabulation/tabulator_verify.html", {
        "meet": meet,
        "verification": verification,
    })
