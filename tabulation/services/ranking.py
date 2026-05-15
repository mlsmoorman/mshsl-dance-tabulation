from collections import defaultdict
from django.db import models
from judging.models import JudgeScoreSheet
from tabulation.services.tiebreakers import apply_tiebreakers

def compute_rankings(meet, division):
    """
    Returns a list of:
    {
        "entry": TeamEntry,
        "judge_ranks": {judge_id: rank},
        "rank_points": int,
        "total_score": float,
        "placement": int,
    }
    """

    # 1. Get entries for this division
    entries = (
        meet.teamentry_set
        .filter(is_active=True, division=division)
        .select_related("team")
    )

    # 2. Build judge -> [(entry, total_score)]
    judge_scores = defaultdict(list)

    for entry in entries:
        sheets = (
            JudgeScoreSheet.objects
            .filter(team_entry=entry, verified=True)
            .select_related("judge")
        )

        for sheet in sheets:
            judge_scores[sheet.judge_id].append((entry, sheet.total))

    # 3. Rank teams per judge
    judge_ranks = defaultdict(dict)

    for judge_id, scores in judge_scores.items():
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

            judge_ranks[judge_id][entry.id] = rank
            last_score = score

    # 4. Compute rank points per entry
    results = []

    for entry in entries:
        ranks = {
            j: judge_ranks[j][entry.id]
            for j in judge_ranks
            if entry.id in judge_ranks[j]
        }

        rank_points = sum(ranks.values())

        total_score = (
            entry.judgescoresheet_set
            .filter(verified=True)
            .aggregate(total=models.Sum("total"))
        )["total"] or 0

        results.append({
            "entry": entry,
            "judge_ranks": ranks,
            "rank_points": rank_points,
            "total_score": total_score,
        })

    # 5. Sort by rank points
    results.sort(key=lambda r: r["rank_points"])

    # 6. Apply tie-breakers
    results = apply_tiebreakers(results)

    # 7. Assign placements
    for i, r in enumerate(results, start=1):
        r["placement"] = i

    return results
