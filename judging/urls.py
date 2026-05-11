from django.urls import path
from .views import superior_judge_review, judge_score_entry

urlpatterns = [
	path("superior-judge/review/<int:team_entry_id>/", superior_judge_review, name="superior_judge_review"),
 	path("judge/score/<int:team_entry_id>/", judge_score_entry, name="judge_score_entry"),
]
