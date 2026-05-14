from django.shortcuts import get_object_or_404, redirect, render
from .models import DQEntry
from .forms import DQEntryForm
from meets.models.entry import TeamEntry


def create_dq(request, entry_id):
    team_entry = get_object_or_404(TeamEntry, id=entry_id)

    if request.method == "POST":
        form = DQEntryForm(request.POST)
        if form.is_valid():
            dq = form.save(commit=False)
            dq.team_entry = team_entry
            dq.reported_by = request.user
            dq.save()
            return redirect("superior:review", entry_id=team_entry.id)
    else:
        form = DQEntryForm()

    return render(request, "superior/create_dq.html", {
        "form": form,
        "team_entry": team_entry,
    })


def confirm_dq(request, dq_id):
    dq = get_object_or_404(DQEntry, id=dq_id)
    dq.confirm(request.user)
    return redirect("superior:review", entry_id=dq.team_entry.id)


def reject_dq(request, dq_id):
    dq = get_object_or_404(DQEntry, id=dq_id)
    dq.reject(request.user)
    return redirect("superior:review", entry_id=dq.team_entry.id)
