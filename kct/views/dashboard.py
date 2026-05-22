from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from meets.models.assignments import KCTAssignment
from meets.models import TeamEntry
from kct.models import KCTEntry


@login_required
def kct_dashboard(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)

    # Load KCT assignments in order
    assignments = (
        KCTAssignment.objects
        .filter(meet=meet)
        .select_related("kct")
        .order_by("kct_number")
    )

    kct_map = {a.kct_id: a.kct_number for a in assignments}
    kct_numbers = [a.kct_number for a in assignments]

    # All entries in this division
    entries = (
        TeamEntry.objects
        .filter(meet=meet, division=division)
        .select_related("team")
        .order_by("performance_order")
    )

    # All KCT entries
    kct_entries = (
        KCTEntry.objects
        .filter(team_entry__meet=meet, team_entry__division=division)
        .select_related("team_entry", "team_entry__team")
    )

    # Group by entry → kct_number → KCTEntry
    kct_by_entry = {}

    for ke in kct_entries:
        entry_id = ke.team_entry_id
        kct_number = kct_map.get(ke.kct_id)

        if entry_id not in kct_by_entry:
            kct_by_entry[entry_id] = {}

        kct_by_entry[entry_id][kct_number] = ke

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
