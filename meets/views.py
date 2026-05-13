from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Meet, TeamEntry, Division
from judging.models import JudgeScoreSheet


@login_required
def tabulator_dashboard(request, pk):
    meet = get_object_or_404(Meet, id=pk)

    # All entries for this meet
    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school")
    )

    # Build data rows
    data = []
    for entry in entries:
        total = (
            JudgeScoreSheet.objects
            .filter(team_entry=entry)
            .aggregate(total=Sum("total"))
            .get("total") or 0
        )

        data.append({
            "entry": entry,
            "team": entry.team,
            "school": entry.team.school,
            "division": entry.division,
            "order": entry.performance_order,
            "verified": entry.verified_by_tabulator,
            "total": total,
        })

    # Split by division
    jazz = [d for d in data if d["division"] == Division.JAZZ]
    kick = [d for d in data if d["division"] == Division.KICK]

    # Sort by total descending
    jazz.sort(key=lambda d: d["total"], reverse=True)
    kick.sort(key=lambda d: d["total"], reverse=True)

    return render(request, "meets/tabulator_dashboard.html", {
        "meet": meet,
        "jazz_entries": jazz,
        "kick_entries": kick,
    })
