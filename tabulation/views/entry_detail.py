from django.shortcuts import render, get_object_or_404
from meets.models import TeamEntry
from judging.models import JudgeScoreSheet
from kct.models import KCTEntry

def entry_detail(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    judge_sheets = JudgeScoreSheet.objects.filter(team_entry=entry)
    kct_entries = KCTEntry.objects.filter(team_entry=entry)

    return render(request, "tabulation/entry_detail.html", {
        "entry": entry,
        "judge_sheets": judge_sheets,
        "kct_entries": kct_entries,
    })
