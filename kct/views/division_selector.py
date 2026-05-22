from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from core.utils import get_kct_division_summary


@login_required
def division_selector(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    summary = get_kct_division_summary(meet)

    return render(request, "kct/division_selector.html", {
        "meet": meet,
        "divisions": summary["divisions"],
        "division_counts": summary["division_counts"],
        "kct_assigned_count": summary["kct_assigned_count"],
        "pending_counts": summary["pending_counts"],
    })
