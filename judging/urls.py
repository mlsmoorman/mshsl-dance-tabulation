from django.urls import path
from .views.home_dashboard import judge_home
from .views.dashboard import judge_dashboard   
from .views import dashboard, view_score_sheets, issues

app_name = "judging"

urlpatterns = [
    path("", judge_home, name="home"),  
    path("meet/<int:meet_id>/", judge_dashboard, name="judge_dashboard"),  
    path("score-sheets/<int:entry_id>/", view_score_sheets.view_score_sheets, name="view_score_sheets"),
    path("flag-issue/<int:entry_id>/", issues.judge_flag_issue, name="judge_flag_issue"),
]

