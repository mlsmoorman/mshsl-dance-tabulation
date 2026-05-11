from django.urls import path
from .views import tabulator_dashboard, tabulator_verify

urlpatterns = [
    path("<int:meet_id>/", tabulator_dashboard, name="tabulator_dashboard"),
    path("verify/<int:team_entry_id>/", tabulator_verify, name="tabulator_verify"),
]
