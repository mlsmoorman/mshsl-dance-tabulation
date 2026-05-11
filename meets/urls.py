from django.urls import path
from .views import tabulator_dashboard, run_prelims_ranking, advance_finalists, run_finals_ranking

path("tabulator/<int:meet_id>/<str:division>/", views.tabulator_dashboard, name="tabulator_dashboard"),
path("tabulator/<int:meet_id>/<str:division>/run_prelims/", views.run_prelims_ranking, name="run_prelims_ranking"),
path("tabulator/<int:meet_id>/<str:division>/advance_finalists/", views.advance_finalists, name="advance_finalists"),
path("tabulator/<int:meet_id>/<str:division>/run_finals/", views.run_finals_ranking, name="run_finals_ranking"),
