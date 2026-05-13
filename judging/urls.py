from django.urls import path
from . import views

app_name = "judging"

urlpatterns = [
    path("meet/<int:meet_id>/my-sheets/", views.judge_meet_sheets, name="judge_meet_sheets"),
    path("sheet/<int:pk>/edit/", views.edit_score_sheet, name="edit_score_sheet"),
]

urlpatterns += [
    path("meet/<int:meet_id>/superior-review/", views.superior_review, name="superior_review"),
]
