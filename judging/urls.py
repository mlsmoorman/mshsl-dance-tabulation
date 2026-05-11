from django.urls import path
from .views import judge_score_entry

urlpatterns = [
 	path("judge/score/<int:team_entry_id>/", judge_score_entry, name="judge_score_entry"),
]
