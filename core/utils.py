# core/utils.py

from meets.models import TeamEntry
from meets.models.assignments import KCTAssignment
from kct.models import KCTEntry


def get_kct_data(meet, division):
    """
    Dashboard-level KCT loader.
    Loads assignments, numbers, and KCTEntry objects grouped by entry.
    """

    assignments = (
        KCTAssignment.objects
        .filter(meet=meet)
        .select_related("kct")
        .order_by("kct_number")
    )

    kct_map = {a.kct_id: a.kct_number for a in assignments}
    kct_numbers = [a.kct_number for a in assignments]

    kct_entries = (
        KCTEntry.objects
        .filter(team_entry__meet=meet, team_entry__division=division)
        .select_related("team_entry", "team_entry__team")
    )

    kct_by_entry = {}

    for ke in kct_entries:
        entry_id = ke.team_entry_id
        kct_number = kct_map.get(ke.kct_id)

        if entry_id not in kct_by_entry:
            kct_by_entry[entry_id] = {}

        kct_by_entry[entry_id][kct_number] = ke

    return {
        "assignments": assignments,
        "kct_numbers": kct_numbers,
        "kct_by_entry": kct_by_entry,
    }


def get_kct_division_summary(meet):
    divisions = ["JAZZ", "KICK"]

    # Team counts per division
    division_counts = {
        d: TeamEntry.objects.filter(meet=meet, division=d).count()
        for d in divisions
    }

    # KCTs assigned (same for both divisions)
    kct_assigned_count = KCTAssignment.objects.filter(meet=meet).count()

    # Pending = KCTEntry exists but kick_count not filled in
    pending_counts = {
        d: KCTEntry.objects.filter(
            team_entry__meet=meet,
            team_entry__division=d,
            kick_count__isnull=True
        ).count()
        for d in divisions
    }

    return {
        "division_counts": division_counts,
        "kct_assigned_count": kct_assigned_count,
        "pending_counts": pending_counts,
        "divisions": divisions,
    }


