from django.shortcuts import render, get_object_or_404
from meets.models.meet import Meet
from meets.models import TeamEntry
from meets.models.assignments import JudgeAssignment, KCTAssignment
from judging.models import JudgeScoreSheet
from kct.models import KCTEntry
from collections import defaultdict

def meet_overview(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    divisions = (
        TeamEntry.objects
        .filter(meet=meet)
        .values_list("division", flat=True)
        .distinct()
    )

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

    division_data = []
    meet_missing_judges = 0
    meet_missing_kcts = 0
    meet_conflicts = 0
    meet_entries = 0

    for division in divisions:
        entries = TeamEntry.objects.filter(meet=meet, division=division)
        entry_count = entries.count()
        meet_entries += entry_count

        sheets = JudgeScoreSheet.objects.filter(team_entry__in=entries)
        sheets_by_entry = defaultdict(dict)
        for s in sheets:
            sheets_by_entry[s.team_entry_id][s.judge_id] = s

        kcts = KCTEntry.objects.filter(team_entry__in=entries)
        kct_by_entry = defaultdict(dict)
        for k in kcts:
            kct_by_entry[k.team_entry_id][k.kct_id] = k

        missing_judges = 0
        missing_kcts = 0
        conflicts = 0

        for entry in entries:
            entry_sheets = sheets_by_entry.get(entry.id, {})
            entry_kcts = kct_by_entry.get(entry.id, {})

            for a in judge_assignments:
                if a.judge_id not in entry_sheets:
                    missing_judges += 1

            for a in kct_assignments:
                if a.kct_id not in entry_kcts:
                    missing_kcts += 1

            if len(kct_assignments) >= 2:
                k1 = entry_kcts.get(kct_assignments[0].kct_id)
                k2 = entry_kcts.get(kct_assignments[1].kct_id)
                if k1 and k2 and k1.illegal != k2.illegal:
                    conflicts += 1

        meet_missing_judges += missing_judges
        meet_missing_kcts += missing_kcts
        meet_conflicts += conflicts

        total_judge_slots = entry_count * judge_assignments.count()
        total_kct_slots = entry_count * kct_assignments.count()

        judge_progress = 100 - int((missing_judges / total_judge_slots) * 100) if total_judge_slots else 100
        kct_progress = 100 - int((missing_kcts / total_kct_slots) * 100) if total_kct_slots else 100

        if conflicts > 0:
            status = "danger"
        elif missing_judges > 0 or missing_kcts > 0:
            status = "warning"
        else:
            status = "success"

        division_data.append({
            "division": division,
            "entries": entry_count,
            "missing_judges": missing_judges,
            "missing_kcts": missing_kcts,
            "conflicts": conflicts,
            "judge_progress": judge_progress,
            "kct_progress": kct_progress,
            "status": status,
        })

    division_data.sort(key=lambda d: (d["status"], -(d["missing_judges"] + d["missing_kcts"] + d["conflicts"])))

    return render(request, "tabulation/meet_overview.html", {
        "meet": meet,
        "division_data": division_data,
        "judge_assignments": judge_assignments,
        "kct_assignments": kct_assignments,
        "meet_entries": meet_entries,
        "meet_missing_judges": meet_missing_judges,
        "meet_missing_kcts": meet_missing_kcts,
        "meet_conflicts": meet_conflicts,
    })

