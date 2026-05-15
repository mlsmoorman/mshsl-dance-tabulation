from judging.models.judge_score_sheet import JudgeScoreSheet
from .kct_deductions import compute_kct_deductions

def apply_kct_deductions(entry):
    d = compute_kct_deductions(entry)

    sheets = JudgeScoreSheet.objects.filter(team_entry=entry)

    for sheet in sheets:
        sheet.time_deduction = d["time"]
        sheet.kick_deduction = d["kick"]
        sheet.other_deduction = d["skill"]

        # Recompute totals
        sheet.subtotal = (
            sheet.choreo_creativity +
            sheet.choreo_visual_effect +
            sheet.diff_routine +
            sheet.diff_formations +
            sheet.diff_skills_or_kicks +
            sheet.exec_placement_control +
            sheet.exec_accuracy +
            sheet.routine_effectiveness +
            (sheet.skills_turns or 0) +
            (sheet.skills_leaps_jumps or 0) +
            (sheet.kicks_technique or 0) +
            (sheet.kicks_height or 0)
        )

        sheet.total = sheet.subtotal - (
            sheet.time_deduction +
            sheet.kick_deduction +
            sheet.other_deduction
        )

        sheet.save()
