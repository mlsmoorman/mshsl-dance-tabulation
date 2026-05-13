from collections import defaultdict
from meets.models import TeamEntry, Division


#~.~.~.~.~.~.~.~.~.~.~.~.~ COMPUTE RANKINGS ~.~.~.~.~.~.~.~.~.~.~.~.~#
def compute_rankings(meet, division):
    # 1. Get all team entries for this division
    entries = TeamEntry.objects.filter(
        meet=meet,
        division=division,
        verified_by_tabulator=True
    )

    # Step 5: Exclude DQ’d teams once meet is locked
    if meet.locked:
        entries = entries.filter(disqualified=False)

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
            else:
                rank += ties
                ties = 0

            judge_ranks[judge][entry.id] = rank
            last_score = score

    # 4. Compute rank points per team
    team_rank_points = defaultdict(int)

    for judge, ranks in judge_ranks.items():
        for entry_id, rank in ranks.items():
            team_rank_points[entry_id] += rank

    # 5. Build final ranking list
    final_list = []

    for entry in entries:
        final_list.append({
            "entry": entry,
            "rank_points": {
                j: judge_ranks[j][entry.id] for j in judge_ranks
            },
            "total_score": entry.total_score(),
        })

    # 6. Sort by total rank points
    final_list.sort(key=lambda x: sum(x["rank_points"].values()))

    # 7. Apply tie breakers
    final_list = apply_tiebreakers(final_list)

    # 8. Assign placements
    placement = 1
    for item in final_list:
        item["placement"] = placement
        placement += 1
        
    return final_list



#~.~.~.~.~.~.~.~.~.~.~.~.~ APPLY TIEBREAKERS ~.~.~.~.~.~.~.~.~.~.~.~.~#
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


#~.~.~.~.~.~.~.~.~.~.~.~.~ SAVE FINAL RESULTS ~.~.~.~.~.~.~.~.~.~.~.~.~#
def save_final_results(meet):
    for division in Division.values:
        ranking = compute_rankings(meet, division)
        for item in ranking:
            entry = item["entry"]
            entry.final_placement = item["placement"]
            entry.final_rank_points = sum(item["rank_points"].values())
            entry.final_total_score = item["total_score"]
            entry.save()


#~.~.~.~.~.~.~.~.~.~.~.~.~ ADVANCE TO FINALS ~.~.~.~.~.~.~.~.~.~.~.~.~#
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


#~.~.~.~.~.~.~.~.~.~.~.~.~ COMPUTE RANK RECAP ~.~.~.~.~.~.~.~.~.~.~.~.~#
def compute_rank_recap(meet, division):
    ranking = compute_rankings(meet, division)

    judges = sorted(next(iter(ranking))["rank_points"].keys()) if ranking else []

    rows = []
    for item in ranking:
        entry = item["entry"]
        rows.append({
            "entry": entry,
            "placement": item["placement"],
            "rank_points": item["rank_points"],  # per judge
            "total_rank_points": sum(item["rank_points"].values()),
            "total_score": item["total_score"],
        })

    return judges, rows
