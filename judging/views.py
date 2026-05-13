from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, 
from django.db.models import Sum
from django.utils import timezone

from meets.models import Meet, TeamEntry, Division
from .models import JudgeScoreSheet, Issue, IssueType
from .services.issue_detection import run_all_issue_detectors
from .forms import JudgeScoreSheetForm


#*****************************************************************************UPDATES:
#~.~.~.~.~.~.~.~.~.~.~.~.~ JUDGE SCORING VIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def judge_scoring(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)
    if not request.user.has_role("JUDGE"):
        return redirect("/")

    sheet = get_or_create_judge_sheet(entry, request.user)

    if request.method == "POST":
        form = JudgeScoreForm(request.POST, instance=sheet)
        if form.is_valid():
            form.save()
            return redirect("judging:next_entry_for_judge", meet_id=entry.meet.id)
    else:
        form = JudgeScoreForm(instance=sheet)

    return render(request, "judging/scoring.html", {
        "entry": entry,
        "form": form,
    })


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


#*****************************************************************************END UPDATES.



#~.~.~.~.~.~.~.~.~.~.~.~.~ JUDGE MEET SHEETS ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def judge_meet_sheets(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    sheets = (
        JudgeScoreSheet.objects
        .filter(judge=request.user, team_entry__meet=meet)
        .select_related("team_entry__team", "team_entry__team__school")
    )

    return render(request, "judging/judge_meet_sheets.html", {
        "meet": meet,
        "sheets": sheets,
    })

#~.~.~.~.~.~.~.~.~.~.~.~.~ EDIT SCORE SHEET ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def edit_score_sheet(request, pk):
    sheet = get_object_or_404(JudgeScoreSheet, id=pk, judge=request.user)

    if request.method == "POST":
        form = JudgeScoreSheetForm(request.POST, instance=sheet)
        if form.is_valid():
            form.save()
            return redirect("judging:judge_meet_sheets", meet_id=sheet.team_entry.meet.id)
    else:
        form = JudgeScoreSheetForm(instance=sheet)

    return render(request, "judging/edit_score_sheet.html", {
        "sheet": sheet,
        "form": form,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~ SUPERIOR JUDGE REVIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def superior_judge_review(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    # Only superior judges allowed
    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school")
    )

    # Build data rows
    data = []
    for entry in entries:
        run_all_issue_detectors(entry)

        total = (
            entry.score_sheets.aggregate(total=Sum("total")).get("total") or 0
        )

        data.append({
            "entry": entry,
            "team": entry.team,
            "school": entry.team.school,
            "division": entry.division,
            "order": entry.performance_order,
            "total": total,
        })

    # Split by division
    jazz = [d for d in data if d["division"] == Division.JAZZ]
    kick = [d for d in data if d["division"] == Division.KICK]

    # Sort by total descending
    jazz.sort(key=lambda d: d["total"], reverse=True)
    kick.sort(key=lambda d: d["total"], reverse=True)

    return render(request, "judging/superior_judge_review.html", {
        "meet": meet,
        "jazz_entries": jazz,
        "kick_entries": kick,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~ ISSUES DASHBOARD ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def issues_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)

    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    entries = (
        TeamEntry.objects
        .filter(meet=meet)
        .select_related("team", "team__school")
        .prefetch_related("issues")
    )

    issues_by_entry = []
    for entry in entries:
        unresolved = entry.issues.filter(resolved=False).order_by("-created_at")
        if unresolved.exists():
            issues_by_entry.append({
                "entry": entry,
                "issues": unresolved
            })

    return render(request, "judging/issues_dashboard.html", {
        "meet": meet,
        "issues_by_entry": issues_by_entry,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~ RESOLVE ISSUES ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def resolve_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if not request.user.has_role("SUPERIOR"):
        return redirect("/")

    issue.resolved = True
    issue.save()

    return redirect("judging:issues_dashboard", meet_id=issue.team_entry.meet.id)


#~.~.~.~.~.~.~.~.~.~.~.~.~ FLAG ISSUES ~.~.~.~.~.~.~.~.~.~.~.~.~#
@login_required
def flag_issue(request, entry_id):
    entry = get_object_or_404(TeamEntry, id=entry_id)

    Issue.objects.create(
        team_entry=entry,
        flagged_by=request.user,
        issue_type=IssueType.MANUAL,
        message=f"Manual issue flagged by {request.user.username}",
        auto_generated=False,
    )

    return redirect("judging:superior_judge_review", meet_id=entry.meet.id)


#~.~.~.~.~.~.~.~.~.~.~.~.~ DQ REVIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
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

        # Resolve dangerous move issues
        issues.update(resolved=True)

        return redirect("judging:superior_judge_review", meet_id=entry.meet.id)

    return render(request, "judging/dq_review.html", {
        "entry": entry,
        "issues": issues,
    })
    

#~.~.~.~.~.~.~.~.~.~.~.~.~ JUDGE FLAG ISSUE ~.~.~.~.~.~.~.~.~.~.~.~.~#
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

    return render(request, "judging/judge_flag_issue.html", {
        "entry": entry,
    })


#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.