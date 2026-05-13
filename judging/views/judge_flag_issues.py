

#~.~.~.~.~.~.~.~.~.~.~.~.~ JUDGE FLAG ISSUE VIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def judge_flag_issue(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    if not request.user.has_role("JUDGE"):
        return redirect("/")

    if request.method == "POST":
        message = request.POST.get("message")
        Issue.objects.create(
            team_entry=entry,
            issue_type=IssueType.MANUAL_JUDGE,
            auto_generated=False,
            flagged_by=request.user,
            message=message,
        )
        return redirect("judging:judge_scoring", entry_id=entry.id)

    return render(request, "judging/judge_flag_issue.html", {"entry": entry})
