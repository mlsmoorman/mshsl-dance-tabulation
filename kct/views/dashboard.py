# kct_dashboard.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from meets.models import TeamEntry
from core.utils import get_kct_data


@login_required
def kct_dashboard(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)

    # Load shared KCT data
    kct = get_kct_data(meet, division)

    assignments = kct["assignments"]
    kct_numbers = kct["kct_numbers"]
    kct_by_entry = kct["kct_by_entry"]

    # All entries in this division
    entries = (
        TeamEntry.objects
        .filter(meet=meet, division=division)
        .select_related("team")
        .order_by("performance_order")
    )

    # Build rows for template
    rows = []

    for entry in entries:
        entry_kcts = kct_by_entry.get(entry.id, {})

        rows.append({
            "entry": entry,
            "kcts": {num: entry_kcts.get(num) for num in kct_numbers},
            "missing": [num for num in kct_numbers if num not in entry_kcts],
        })

    return render(request, "kct/dashboard.html", {
        "meet": meet,
        "division": division,
        "kct_numbers": kct_numbers,
        "rows": rows,
    })
