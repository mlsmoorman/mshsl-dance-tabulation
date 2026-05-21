from django.urls import path
from .views.home_dashboard import judge_home
from .views.dashboard import judge_dashboard   
from .views.view_score_sheets import view_score_sheets
from .views.issues import judge_flag_issue

app_name = "judging"

urlpatterns = [
    path("", judge_home, name="home"),  
    path("meet/<int:meet_id>/", judge_dashboard, name="judge_dashboard"),  
    path("score-sheets/<int:entry_id>/", view_score_sheets, name="view_score_sheets"),
    path("flag-issue/<int:entry_id>/", judge_flag_issue, name="judge_flag_issue"),
]

