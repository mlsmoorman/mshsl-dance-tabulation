from django.urls import path
from .views import kct_dashboard, kct_entry

urlpatterns = [
    path("meet/<int:meet_id>/", kct_dashboard, name="kct_dashboard"),
    path("entry/<int:entry_id>/", kct_entry, name="kct_entry"),
]
