from django.urls import path
from .views import verify, lock_meet, final_results, announcer, judge_recap

app_name = "tabulation"

urlpatterns = [
    path("meet/<int:meet_id>/verify/", verify.tabulator_verify, name="tabulator_verify"),
    path("meet/<int:meet_id>/lock/", lock_meet.lock_meet, name="lock_meet"),
    path("meet/<int:meet_id>/results/", final_results.final_results, name="final_results"),
    path("meet/<int:meet_id>/announcer/", announcer.announcer_results, name="announcer_results"),
    path("meet/<int:meet_id>/recap/<str:division>/", judge_recap.judge_recap, name="judge_recap"),
]
