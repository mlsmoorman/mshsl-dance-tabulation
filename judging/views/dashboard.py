from django.shortcuts import render, get_object_or_404, redirect
from judging.models import JudgeScoreSheet
from meets.models import Meet, TeamEntry, Division

def judge_dashboard(request, meet_id):
    meet = get_object_or_404(Meet, id=meet_id)
    entries = meet.teamentry_set.filter(is_active=True)

    # Build (entry, sheet) pairs
    entry_sheets = []
    for entry in entries:
        sheet, created = JudgeScoreSheet.objects.get_or_create(
            team_entry=entry,
            judge=request.user,
            defaults={
                "choreo_creativity": 0,
                "choreo_visual_effect": 0,
                "diff_routine": 0,
                "diff_formations": 0,
                "diff_skills_or_kicks": 0,
                "exec_placement_control": 0,
                "exec_accuracy": 0,
                "routine_effectiveness": 0,
                "skills_turns": 0,
                "skills_leaps_jumps": 0,
                "kicks_technique": 0,
                "kicks_height": 0,
                "comments": "",
            }
        )   
        entry_sheets.append((entry, sheet))

    # Handle POST
    if request.method == "POST":
        entry_id = request.POST.get("entry_id")
        entry = get_object_or_404(TeamEntry, id=entry_id)
        sheet = JudgeScoreSheet.objects.get(team_entry=entry, judge=request.user)

        # Shared categories
        sheet.choreo_creativity = int(request.POST.get("choreo_creativity"))
        sheet.choreo_visual_effect = int(request.POST.get("choreo_visual_effect"))
        sheet.diff_routine = int(request.POST.get("diff_routine"))
        sheet.diff_formations = int(request.POST.get("diff_formations"))
        sheet.diff_skills_or_kicks = int(request.POST.get("diff_skills_or_kicks"))
        sheet.exec_placement_control = int(request.POST.get("exec_placement_control"))
        sheet.exec_accuracy = int(request.POST.get("exec_accuracy"))
        sheet.routine_effectiveness = int(request.POST.get("routine_effectiveness"))

        # Jazz vs Kick
        if entry.division == Division.JAZZ:
            sheet.skills_turns = int(request.POST.get("skills_turns"))
            sheet.skills_leaps_jumps = int(request.POST.get("skills_leaps_jumps"))
        else:
            sheet.kicks_technique = int(request.POST.get("kicks_technique"))
            sheet.kicks_height = int(request.POST.get("kicks_height"))

        # Comments
        sheet.comments = request.POST.get("comments")

        sheet.save()
        return redirect("judging:judge_dashboard", meet_id=meet_id)

    return render(request, "judging/judge_score_entry.html", {
        "meet": meet,
        "entry_sheets": entry_sheets,
    })
