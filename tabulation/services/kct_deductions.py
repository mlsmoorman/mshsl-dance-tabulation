def compute_kct_deductions(entry):
    deductions = {
        "time": 0,
        "kick": 0,
        "skill": 0,
    }

    # TIME DEDUCTION
    if entry.kct_entry.routine_time_seconds:
        if entry.kct_entry.routine_time_seconds < 90:
            deductions["time"] = 1.0
        elif entry.kct_entry.routine_time_seconds > 120:
            deductions["time"] = 1.0

    # KICK DEDUCTION
    if entry.division == "KICK" and entry.kct_entry.kick_count is not None:
        required = 40
        if entry.kct_entry.kick_count < required:
            deductions["kick"] = (required - entry.kct_entry.kick_count) * 0.1

    # JAZZ SKILL DEDUCTION
    if entry.division == "JAZZ":
        if not entry.kct_entry.jazz_team_turn_performed:
            deductions["skill"] += 1.0
        if not entry.kct_entry.jazz_leap_jump_performed:
            deductions["skill"] += 1.0

    return deductions
