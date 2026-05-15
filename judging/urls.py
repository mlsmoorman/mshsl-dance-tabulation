from django.urls import path
from .views import dashboard
from .views import view_score_sheets

urlpatterns = [
    path(
        "meet/<int:meet_id>/",
        dashboard.judge_dashboard,
        name="judge_dashboard"
    ),
    path(
        "score-sheets/<int:entry_id>/",
        view_score_sheets.view_score_sheets,
        name="view_score_sheets"
    ),
]
