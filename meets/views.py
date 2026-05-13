from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Meet, TeamEntry
from judging.models import JudgeScoreSheet
from .models import Division


@login_required
def tabulator_dashboard(request, pk):
    meet = get_object_or_404(Meet, id=pk)
    entries = TeamEntry.objects.filter(meet=meet).select_related("team", "team__school")

    # Aggregate totals per entry
    data = []
    for entry in entries:
        sheets = JudgeScoreSheet.objects.filter(team_entry=entry)
        total = sum(s.total for s in sheets)
        data.append({
            "entry": entry,
            "sheets": sheets,
            "total": total,
        })

    # Split by division
    jazz = [d for d in data if d["entry"].division == Division.JAZZ]
    kick = [d for d in data if d["entry"].division == Division.KICK]

    # Sort by total descending
    jazz.sort(key=lambda d: d["total"], reverse=True)
    kick.sort(key=lambda d: d["total"], reverse=True)

    return render(request, "meets/tabulator_dashboard.html", {
        "meet": meet,
        "jazz_entries": jazz,
        "kick_entries": kick,
    })
