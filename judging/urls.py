from django.urls import path
from . import views

app_name = "judging"


#~.~.~.~.~.~.~.~.~.~.~.~.~ JUDGE MEET SHEETS / EDIT SCORE SHEET ~.~.~.~.~.~.~.~.~.~.~.~.~#
urlpatterns = [
    path("meet/<int:meet_id>/my-sheets/", views.judge_meet_sheets, name="judge_meet_sheets"),
    path("sheet/<int:pk>/edit/", views.edit_score_sheet, name="edit_score_sheet"),
    path("entry/<int:entry_id>/judge-flag/", views.judge_flag_issue, name="judge_flag_issue"),
]


#~.~.~.~.~.~.~.~.~.~.~.~.~ SUPERIOR JUDGE REVIEW ~.~.~.~.~.~.~.~.~.~.~.~.~#
urlpatterns += [
    path("meet/<int:meet_id>/superior-review/", views.superior_judge_review, name="superior_review"),
]


#~.~.~.~.~.~.~.~.~.~.~.~.~ ISSUES / RESOVLE / FLAG ~.~.~.~.~.~.~.~.~.~.~.~.~#
urlpatterns += [
    path("meet/<int:meet_id>/issues/", views.issues_dashboard, name="issues_dashboard"),
    path("issue/<int:issue_id>/resolve/", views.resolve_issue, name="resolve_issue"),
    path("entry/<int:entry_id>/flag/", views.flag_issue, name="flag_issue"),
]
