from django.shortcuts import render, get_object_or_404
from meets.models.entry import TeamEntry
from kct.models import KCTEntry

def kct_entry(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    kct, created = KCTEntry.objects.get_or_create(team_entry=entry)

    return render(request, "kct/entry.html", {
        "entry": entry,
        "kct": kct,
    })
