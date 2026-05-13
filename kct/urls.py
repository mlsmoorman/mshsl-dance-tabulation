from django.urls import path
from .views import dashboard, entry, dangerous_move

app_name = "kct"

urlpatterns = [
    path("meet/<int:meet_id>/", dashboard.kct_dashboard, name="dashboard"),
    path("entry/<int:entry_id>/", entry.kct_entry_form, name="entry_form"),
    path("dangerous/<int:entry_id>/", dangerous_move.mark_dangerous_move, name="dangerous_move"),
]
