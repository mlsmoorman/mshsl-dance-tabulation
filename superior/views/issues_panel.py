#  ✔ Superior Judge Workflow
#  superior/views/review.py
#  superior/views/issues_panel.py
#  superior/views/dq_review.py
#  • Review KCT data
#  • Review judge sheets
#  • Review issues
#  • Resolve issues
#  • DQ review
#  • DQ execution

#~.~.~.~.~.~.~.~.~.~.~.~.~ ISSUES DASHBOARD VIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def issues_dashboard(request, meet_id):
    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)
    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .prefetch_related("issues")
    )

    issues_by_entry = [
        {"entry": e, "issues": e.issues.filter(resolved=False)}
        for e in entries
        if e.issues.filter(resolved=False).exists()
    ]

    return render(request, "superior/issues_dashboard.html", {
        "meet": meet,
        "issues_by_entry": issues_by_entry,
    })



#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#