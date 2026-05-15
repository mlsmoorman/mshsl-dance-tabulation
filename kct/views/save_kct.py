from django.shortcuts import redirect, get_object_or_404
from meets.models.entry import TeamEntry
from kct.models import KCTEntry
from tabulation.services.apply_kct_to_scores import apply_kct_deductions

def save_kct(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    kct, created = KCTEntry.objects.get_or_create(team_entry=entry)

    kct.num_competitors = request.POST.get("num_competitors") or None
    kct.routine_time_seconds = request.POST.get("routine_time_seconds") or None
    kct.kick_count = request.POST.get("kick_count") or None

    kct.jazz_team_turn_performed = bool(request.POST.get("jazz_team_turn_performed"))
    kct.jazz_leap_jump_performed = bool(request.POST.get("jazz_leap_jump_performed"))

    kct.falls_observed = request.POST.get("falls_observed") or 0
    kct.dangerous_move_observed = bool(request.POST.get("dangerous_move_observed"))

    kct.save()

    apply_kct_deductions(entry)

    return redirect("kct_dashboard", meet_id=entry.meet.id)
