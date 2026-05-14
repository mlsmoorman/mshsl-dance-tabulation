from django.shortcuts import redirect, get_object_or_404
from ..models import KCTEntry


def mark_dangerous_move(request, entry_id):
    entry = get_object_or_404(KCTEntry, id=entry_id)
    entry.dangerous_move_observed = True
    entry.save()
    return redirect("kct:dashboard", meet_id=entry.team_entry.meet.id)
