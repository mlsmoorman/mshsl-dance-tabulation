from django.urls import path
from .views.dashboard import tabulator_dashboard
from .views.verify import tabulator_verify
from .views.meet_overview import meet_overview
from .views.lock_meet import lock_meet
from .views.results import meet_results
from .views.announcer import announcer_results
from .views.judge_recap import judge_recap
from .views.reorder_entries import reorder_entries
from .views.public_results import public_results

app_name = "tabulation"

urlpatterns = [
    path("", tabulator_dashboard, name="dashboard"),
    path("meet/<int:meet_id>/verify/", tabulator_verify, name="tabulator_verify"),
    path("meet/<int:meet_id>/", meet_overview, name="meet_overview"),
    path("meet/<int:meet_id>/lock/", lock_meet, name="lock_meet"),
    path("meet/<int:meet_id>/results/", meet_results, name="final_results"),
    path("meet/<int:meet_id>/announcer/", announcer_results, name="announcer_results"),
    path("meet/<int:meet_id>/recap/<str:division>/", judge_recap, name="judge_recap"),
    path("reorder-entries/", reorder_entries, name="reorder_entries"),
    path("public-results/<int:meet_id>/", public_results, name="public_results"),
]
