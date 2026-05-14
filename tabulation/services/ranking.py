def compute_rankings(meet):
    """
    Returns a list of:
    {
        "entry": TeamEntry,
        "rank": int,
        "placement": int,
        "rank_points": int,
        "total_score": float,
    }
    """

    entries = meet.teamentry_set.filter(is_active=True)

    # Placeholder scoring logic — replace with real scoring later
    results = []
    for entry in entries:
        total_score = entry.total_score if hasattr(entry, "total_score") else 0
        results.append({
            "entry": entry,
            "total_score": total_score,
        })

    # Sort by score descending
    results.sort(key=lambda r: r["total_score"], reverse=True)

    # Assign ranks
    for i, r in enumerate(results, start=1):
        r["rank"] = i
        r["placement"] = i
        r["rank_points"] = len(results) - i + 1

    return results
