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

#~.~.~.~.~.~.~.~.~.~.~.~.~ DQ REVIEW VIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def dq_review(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    issues = entry.issues.filter(issue_type=IssueType.DANGEROUS_MOVE, resolved=False)

    if request.method == "POST":
        reason = request.POST.get("reason")
        entry.disqualified = True
        entry.dq_reason = reason
        entry.dq_timestamp = timezone.now()
        entry.dq_by = request.user
        entry.save()
        issues.update(resolved=True)
        return redirect("superior:superior_review", meet_id=entry.meet.id)

    return render(request, "superior/dq_review.html", {
        "entry": entry,
        "issues": issues,
    })



#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#