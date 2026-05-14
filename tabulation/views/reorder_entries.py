from django.http import JsonResponse
from django.views.decorators.http import require_POST
from meets.models.entry import TeamEntry

@require_POST
def reorder_entries(request):
    """
    Receives JSON:
    {
        "entry_ids": [5, 2, 9, 1]
    }
    And updates performance_order based on the new order.
    """
    entry_ids = request.POST.getlist("entry_ids[]")

    for index, entry_id in enumerate(entry_ids, start=1):
        TeamEntry.objects.filter(id=entry_id).update(performance_order=index)

    return JsonResponse({"status": "ok"})
