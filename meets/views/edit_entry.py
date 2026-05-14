from django.shortcuts import render, redirect, get_object_or_404
from meets.models.entry import TeamEntry
from meets.forms import TeamEntryForm

def edit_entry(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    if request.method == "POST":
        form = TeamEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("meet_overview", meet_id=entry.meet.id)
    else:
        form = TeamEntryForm(instance=entry)

    return render(request, "meets/edit_entry.html", {
        "entry": entry,
        "form": form,
    })
