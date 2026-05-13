from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from ..services.rankings import save_final_results


@login_required
def lock_meet(request, meet_id):
    if not request.user.has_role("TABULATOR"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)
    meet.locked = True
    meet.locked_at = timezone.now()
    meet.locked_by = request.user
    meet.save()

    save_final_results(meet)

    return redirect("tabulation:final_results", meet_id=meet.id)
