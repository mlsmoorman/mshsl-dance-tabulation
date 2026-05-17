from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from meets.models.meet import Meet
from ..services.ranking import compute_rankings


@login_required
def judge_recap(request, meet_id, division):
    meet = get_object_or_404(Meet, id=meet_id)
    ranking = compute_rankings(meet, division)

    judges = sorted(next(iter(ranking))["rank_points"].keys()) if ranking else []

    rows = []
    for item in ranking:
        rows.append({
            "entry": item["entry"],
            "placement": item["placement"],
            "rank_points": item["rank_points"],
            "total_rank_points": sum(item["rank_points"].values()),
            "total_score": item["total_score"],
        })

    return render(request, "tabulation/judge_recap.html", {
        "meet": meet,
        "division": division,
        "judges": judges,
        "rows": rows,
    })


