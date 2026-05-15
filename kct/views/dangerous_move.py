from django.shortcuts import redirect, get_object_or_404
from meets.models.entry import TeamEntry
from kct.models import KCTEntry

def report_dangerous_move(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    kct, created = KCTEntry.objects.get_or_create(team_entry=entry)

    kct.dangerous_move_observed = True
    kct.save()

    return redirect("kct_entry", entry_id=entry.id)
