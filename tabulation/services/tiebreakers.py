def apply_tiebreakers(final_list):
    """
    Applies MSHSL tie-breakers to a list of ranking dicts.
    Each dict must contain:
        - "judge_ranks": {judge_id: rank}
        - "rank_points": int
        - "total_score": float
    """

    changed = True

    while changed:
        changed = False

        for i in range(len(final_list) - 1):
            a = final_list[i]
            b = final_list[i + 1]

            # Only compare tied rank points
            if a["rank_points"] != b["rank_points"]:
                continue

            # 1. Most judges ranking higher
            a_better = sum(
                1 for j in a["judge_ranks"]
                if a["judge_ranks"][j] < b["judge_ranks"].get(j, 999)
            )
            b_better = sum(
                1 for j in b["judge_ranks"]
                if b["judge_ranks"][j] < a["judge_ranks"].get(j, 999)
            )

            if a_better < b_better:
                final_list[i], final_list[i + 1] = b, a
                changed = True
                continue

            if a_better == b_better:
                # 2. Lowest single judge rank
                if min(a["judge_ranks"].values()) > min(b["judge_ranks"].values()):
                    final_list[i], final_list[i + 1] = b, a
                    changed = True
                    continue

                if min(a["judge_ranks"].values()) == min(b["judge_ranks"].values()):
                    # 3. Highest total score
                    if a["total_score"] < b["total_score"]:
                        final_list[i], final_list[i + 1] = b, a
                        changed = True
                        continue

    return final_list
