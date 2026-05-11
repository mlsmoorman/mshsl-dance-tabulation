from django.urls import path
from .views import run_prelims_ranking, advance_finalists, run_finals_ranking

urlpatterns = [
    path("tabulator/<int:meet_id>/<str:division>/run_prelims/", run_prelims_ranking, name="run_prelims_ranking"),
    path("tabulator/<int:meet_id>/<str:division>/advance_finalists/", advance_finalists, name="advance_finalists"),
    path("tabulator/<int:meet_id>/<str:division>/run_finals/", run_finals_ranking, name="run_finals_ranking"),
]
