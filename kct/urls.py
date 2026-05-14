from django.urls import path
from .views.dashboard import kct_dashboard
from .views.entry import kct_entry_form
from .views.dangerous_move import mark_dangerous_move

app_name = "kct"

urlpatterns = [
    path("meet/<int:meet_id>/", kct_dashboard, name="dashboard"),
    path("entry/<int:entry_id>/", kct_entry_form, name="entry_form"),
    path("dangerous/<int:entry_id>/", mark_dangerous_move, name="dangerous_move"),
]

