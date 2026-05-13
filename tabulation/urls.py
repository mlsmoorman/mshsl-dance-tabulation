from django.urls import path
from .views import tabulator_dashboard, tabulator_verify, lock_meet


urlpatterns = [
    path("meet/<int:meet_id>/verify/", tabulator_verify, name="tabulator_verify"),
    path("meet/<int:meet_id>/lock/", lock_meet, name="lock_meet"),
]
