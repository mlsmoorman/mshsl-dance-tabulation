from django.urls import path
from .views import dashboard, score_sheet

app_name = "judging"

urlpatterns = [
    path("meet/<int:meet_id>/", dashboard.judge_dashboard, name="dashboard"),
    path("entry/<int:entry_id>/", score_sheet.judge_score_sheet, name="score_sheet"),
]
