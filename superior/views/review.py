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

#~.~.~.~.~.~.~.~.~.~.~.~.~ SUPERIOR REVIEW VIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def superior_review(request, meet_id):
    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    meet = get_object_or_404(Meet, id=meet_id)
    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school", "kctentry")
        .prefetch_related("issues", "judgesscoresheet_set")
        .order_by("performance_order")
    )

    return render(request, "superior/review.html", {
        "meet": meet,
        "entries": entries,
    })



#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#