from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from kct.models import KCTEntry
from meets.models.assignments import JudgeAssignment, KCTAssignment
from judging.models.judge_score_sheet import JudgeScoreSheet


@login_required
def tabulator_verify(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)
    ...

    division = request.GET.get("division")  # or pass it as a URL parameter

    judge_assignments = (
        JudgeAssignment.objects
        .filter(meet=meet)
        .select_related("judge")
        .order_by("judge_number")
    )

    kct_assignments = (
        KCTAssignment.objects
        .filter(meet=meet)
        .select_related("kct")
        .order_by("kct_number")
    )

    judge_map = {a.judge_id: a.judge_number for a in judge_assignments}
    kct_map = {a.kct_id: a.kct_number for a in kct_assignments}

    judge_numbers = [a.judge_number for a in judge_assignments]
    kct_numbers = [a.kct_number for a in kct_assignments]

    entries = (
        TeamEntry.objects
        .filter(meet=meet, division=division)
        .select_related("team")
        .order_by("performance_order")
    )

    sheets = (
        JudgeScoreSheet.objects
        .filter(team_entry__meet=meet, team_entry__division=division)
        .select_related("judge", "team_entry")
    )


    sheets_by_entry = {}

    for sheet in sheets:
        entry_id = sheet.team_entry_id
        judge_number = judge_map.get(sheet.judge_id)

        if entry_id not in sheets_by_entry:
            sheets_by_entry[entry_id] = {}

        sheets_by_entry[entry_id][judge_number] = sheet

    # Load all KCT entries and group them
    kct_entries = (
        KCTEntry.objects
        .filter(team_entry__meet=meet, team_entry__division=division)
        .select_related("kct", "team_entry")
    )

    kct_by_entry = {}

    for ke in kct_entries:
        entry_id = ke.team_entry_id
        kct_number = kct_map.get(ke.kct_id)

        if entry_id not in kct_by_entry:
            kct_by_entry[entry_id] = {}

        kct_by_entry[entry_id][kct_number] = ke

    # Build verification rows
    rows = []

    for entry in entries:
        entry_id = entry.id

        judge_data = sheets_by_entry.get(entry_id, {})
        kct_data = kct_by_entry.get(entry_id, {})

        missing_judges = [j for j in judge_numbers if j not in judge_data]
        missing_kcts = [k for k in kct_numbers if k not in kct_data]

        # KCT conflict detection
        kct_conflicts = False
        if len(kct_numbers) >= 2:
            k1 = kct_data.get(1)
            k2 = kct_data.get(2)
            if k1 and k2:
                if k1.illegal != k2.illegal:
                    kct_conflicts = True

        rows.append({
            "entry": entry,
            "judge_sheets": {j: judge_data.get(j) for j in judge_numbers},
            "kct_entries": {k: kct_data.get(k) for k in kct_numbers},
            "missing_judges": missing_judges,
            "missing_kcts": missing_kcts,
            "kct_conflicts": kct_conflicts,
        })


    return render(request, "tabulation/verify.html", {
        "meet": meet,
        "division": division,
        "judge_numbers": judge_numbers,
        "kct_numbers": kct_numbers,
        "rows": rows,
    })
