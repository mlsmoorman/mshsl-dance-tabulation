from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from tabulation.models import MeetLock, FinalResult
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from tabulation.services.ranking import compute_rankings

def lock_meet(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    # Prevent double-locking
    if MeetLock.objects.filter(meet=meet).exists():
        return redirect("meet_results", meet_id=meet.id)

    # Create lock record
    MeetLock.objects.create(
        meet=meet,
        locked_by=request.user if request.user.is_authenticated else None,
        locked_at=timezone.now()
    )

    # Run ranking engine
    rankings = compute_rankings(meet)

    # Save final results snapshot
    for result in rankings:
        FinalResult.objects.create(
            meet=meet,
            entry=result["entry"],
            final_rank=result["rank"],
            final_placement=result["placement"],
            final_rank_points=result["rank_points"],
            final_total_score=result["total_score"],
        )

    return redirect("tabulation_results", meet_id=meet.id)
