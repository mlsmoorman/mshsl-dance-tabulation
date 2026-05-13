from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import KCTEntryForm
from meets.models import TeamEntry, Meet
from judging.services.issue_detection import run_all_issue_detectors, get_active_rules

#~.~.~.~.~.~.~.~.~.~.~.~.~ KCT ENTRY ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def kct_entry(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    # Only KCT, Superior Judge, or Tabulator should access
    if not request.user.has_role("KCT") and not request.user.has_role("SUPERIOR"):
        return redirect("/")

    kct = getattr(entry, "kctentry", None)

    if request.method == "POST":
        form = KCTEntryForm(request.POST, instance=kct)
        if form.is_valid():
            kct = form.save(commit=False)
            kct.entry = entry
            kct.save()

            # Run automatic issue detection
            run_all_issue_detectors(entry)

            return redirect("kct:kct_dashboard", meet_id=entry.meet.id)
    else:
        form = KCTEntryForm(instance=kct)

    return render(request, "kct/kct_entry.html", {
        "entry": entry,
        "form": form,
        "rules": get_active_rules(),
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~ KCT DASHBOARD ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def kct_dashboard(request, meet_id):
    if not request.user.has_role("KCT"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)
    entries = meet.entries.select_related("team").all()

    return render(request, "kct/kct_dashboard.html", {
        "meet": meet,
        "entries": entries,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#
