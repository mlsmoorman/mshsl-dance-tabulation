from django.urls import path
from .views import superior_judge_review, tabulator_verify

urlpatterns = [
	path("superior-judge/review/<int:team_entry_id"), superior_judge_review, name="superior_judge_review",
	path("tabulator/verify/<int:team_entry_id/", tabulator_verify, name="tabulator_verify"),
 ]
