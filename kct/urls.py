from django.urls import path
from .views.dashboard import kct_dashboard
from .views.entry import kct_entry
from .views.save_kct import save_kct
from .views.dangerous_move import report_dangerous_move

urlpatterns = [
    path("meet/<int:meet_id>/", kct_dashboard, name="kct_dashboard"),
    path("entry/<int:entry_id>/", kct_entry, name="kct_entry"),
    path("entry/<int:entry_id>/save/", save_kct, name="save_kct"),
    path("entry/<int:entry_id>/dangerous/", report_dangerous_move, name="report_dangerous_move"),
]
