from judging.models import JudgeScoreSheet, KCTEntry

def get_possible_issues(team_entry):
    issues = []
    
    kct = KCTEntry.objects.filter(team_entry=team_entry).order_by("-id").first()
    judge_sheets = JudgeScoreSheet.objects.filter(team_entry=team_entry)
    
    # 1. Kick Count
    if team_entry.division == "KICK" and kct:
        if kct.kick_count is None:
            issues.append("Kick count missing.")
        elif kct.kick_count < 35 or kct.kick_count > 55:
            issues.append(f"Kick count outside normal range ({kct.kick_count}).")
    
    # 2. Routine Time
    if kct:
        t = kct.routine_time_seconds
        if t is None:
            issues.append("Routine time missing.")
        else:
            if team_entry.division == "JAZZ":
                if t < 120 or t > 150:
                    issues.append(f"Routine time outside normal range ({t} seconds).")
                elif abs(t - 120) <= 3 or abs(t - 150) <= 3:
                    issues.append(f"Routine time close to boundary ({t} seconds).")
            else:
                if t < 135 or t > 165:
                    issues.append(f"Routine time outside normal range ({t} seconds).")
                elif abs(t - 135) <= 3 or abs(t - 165) <= 3:
                    issues.append(f"Routine time close to boundary ({t} seconds).")
                    
    # 3. Competitor Count
    if kct and kct.num_competitors is not None:
        if kct.num_competitors < 5 or kct.num_competitors > 40:
            issues.append(f"Competitor count unusual ({kct.num_competitors}).")
            
    # 4. Judge Comments
    keywords = ["fall", "illegal", "dangerous", "prop", "lift", "drop", "stunt", "uniform", "dq"]
    for sheet in judge_sheets:
        if sheet.comments:
            for word in keywords:
                if word in sheet.comments.lower():
                    issues.append(f"Judge {sheet.judge_number} comment mentions '{word}'.")
                    
    # 5. Score discrepancies
    for category in ["performance", "choreography", "execution", "presentation"]:
        scores = [getattr(s, category) for s in judge_sheets if getattr(s, category) is not None]
        if scores:
            if max(scores) - min(scores) > 3:
                issues.append(f"Large discrepance in {category.capitalize()} scores.")
    
    # 6. Missing Judge Sheets
    if judge_sheets.count() < team_entry.meet.num_judges:
        issues.append(f"One or more judge score sheets are missing.")
        
    # 7. Missing KCT Entry
    if not kct:
        issues.append("No KCT entry found.")
        
    return issues