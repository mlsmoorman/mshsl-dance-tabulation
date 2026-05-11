from django.urls import path
from .views import kct_entry

urlpatterns = [
    path("<int:team_entry_id>/", kct_entry, name="kct_entry"),
]
