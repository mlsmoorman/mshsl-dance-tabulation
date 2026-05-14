from django.shortcuts import render, redirect, get_object_or_404
from ..models import KCTEntry
from ..forms import KCTEntryForm
from meets.models.entry import TeamEntry


def kct_entry_form(request, entry_id):
    team_entry = get_object_or_404(TeamEntry, id=entry_id)

    # Get or create the KCT entry for this user
    kct_entry, created = KCTEntry.objects.get_or_create(
        team_entry=team_entry,
        kct=request.user
    )

    other_entry = (
        KCTEntry.objects
        .filter(team_entry=team_entry)
        .exclude(kct=request.user)
        .first()
    )

    if request.method == "POST":
        form = KCTEntryForm(request.POST, instance=kct_entry, team_entry=team_entry)
        if form.is_valid():
            form.save()
            return redirect("kct:dashboard", meet_id=team_entry.meet.id)
    else:
        form = KCTEntryForm(instance=kct_entry, team_entry=team_entry)

    return render(request, "kct/entry_form.html", {
        "form": form,
        "team_entry": team_entry,
        "other_entry": other_entry,
    })
