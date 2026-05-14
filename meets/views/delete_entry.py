from django.shortcuts import redirect, get_object_or_404
from meets.models.entry import TeamEntry

def delete_entry(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    entry.is_active = False
    entry.save()
    return redirect("meet_overview", meet_id=entry.meet.id)
