from collections import defaultdict

def compute_rankings(meet, division):
    # 1. Get all team entries for this division
    entries = meet.teamentry.set.filter(division=division, verified_by_tabulator=True)
    
    # 2. Build judge -> list of (team, score)
    judge_scores = defaultdict(list)
    
    for entry in entries:
        for sheet in entry.judgesscoresheet_set.all():
            judge_scores[sheet.judge.number].append((entry, sheet.total_score))
            
    # 3. Rank teams per judge
    judge_ranks = defaultdict(dict)
    
    for judge, scores in judge_scores.items():
        # Sort descending by score
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        rank = 1
        last_score = None
        ties = 0
        
        for entry, score in sorted_scores:
            if score == last_score:
                ties += 1
                ties = 0
            judge_ranks[judge][entry.id] = rank
            last_score = score
    
    # 4. Compute rank points per team
    team_rank_points = defaultdict(int)
    
    for judge, ranks in judge_ranks.items():
        for entry.id, rank in ranks.items():
            team_rank_points[entry.id] += rank
            
    # 5. Build final ranking list
    final_list = []
    
    for entry in entries:
        final_list.append({
			"entry": entry,
			"rank_points": {j: judge_ranks[j][entry.id] for j in judge_ranks},
			"total_score": entry.total_score(),
		})
        
    # 6. Sort by rank points
    final_list.sort(key=lambda x: x["rank_points"])
    
    # 7. Apply tie breakers
    final_list = apply_tiebreakers(final_list)
    
    return final_list

def apply_tiebreakers(final_list):
    i = 0
    while i < len(final_list) - 1:
        a = final_list[i]
        b = final_list[i + 1]

        if a["rank_points"] == b["rank_points"]:
            # 1. Most judges ranking higher
            a_better = sum(1 for j in a["judge_ranks"] if a["judge_ranks"][j] < b["judge_ranks"][j])
            b_better = sum(1 for j in b["judge_ranks"] if b["judge_ranks"][j] < a["judge_ranks"][j])

            if a_better < b_better:
                final_list[i], final_list[i + 1] = b, a
                continue

            if a_better == b_better:
                # 2. Lowest single judge rank
                if min(a["judge_ranks"].values()) > min(b["judge_ranks"].values()):
                    final_list[i], final_list[i + 1] = b, a
                    continue

                if min(a["judge_ranks"].values()) == min(b["judge_ranks"].values()):
                    # 3. Highest total score
                    if a["total_score"] < b["total_score"]:
                        final_list[i], final_list[i + 1] = b, a
                        continue

        i += 1

    return final_list

def advance_to_finals(meet, division):
    rankings = compute_rankings(meet, division)
    finalists = []
    cutoff = meet.num_finalists
    
    # Select top X teams
    for i, row in enumerate(rankings):
        if i < cutoff:
            finalists.append(row["entry"])
        else:
            # Check for tie at cutoff boundary
            if row["rank_points"] == rankings[cutoff - 1]["rank_points"]:
                finalists.append(row["entry"])
            else:
                break
    
    # Mark finalists
    for entry in meet.teamentry_set.filter(division=division):
        entry.is_finalist = entry in finalists
        entry.save()
    
    return finalists