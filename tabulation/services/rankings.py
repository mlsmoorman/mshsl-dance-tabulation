from collections import defaultdict

from meets.models.entry import TeamEntry
from meets.models.entry import Division  # adjust if Division lives elsewhere
from .tiebreakers import apply_tiebreakers


def compute_rankings(meet, division):
    entries = TeamEntry.objects.filter(
        meet=meet,
        division=division,
        verified_by_tabulator=True,
    )

    if meet.locked:
        entries = entries.filter(disqualified=False)

    judge_scores = defaultdict(list)

    for entry in entries:
        for sheet in entry.judgesscoresheet_set.all():
            judge_scores[sheet.judge.number].append((entry, sheet.total_score))

    judge_ranks = defaultdict(dict)

    for judge, scores in judge_scores.items():
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

    final_list = []

    for entry in entries:
        rank_points = {j: judge_ranks[j][entry.id] for j in judge_ranks}
        final_list.append({
            "entry": entry,
            "rank_points": rank_points,
            "total_score": entry.total_score(),
        })

    final_list.sort(key=lambda x: sum(x["rank_points"].values()))
    final_list = apply_tiebreakers(final_list)

    placement = 1
    for item in final_list:
        item["placement"] = placement
        placement += 1

    return final_list


def save_final_results(meet):
    for division in Division.values:
        ranking = compute_rankings(meet, division)
        for item in ranking:
            entry = item["entry"]
            entry.final_placement = item["placement"]
            entry.final_rank_points = sum(item["rank_points"].values())
            entry.final_total_score = item["total_score"]
            entry.save()

