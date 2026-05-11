from django.urls import path
from .views import superior_judge_review

urlpatterns = [
    path("<int:team_entry_id>/", superior_judge_review, name="superior_judge_review"),
]
