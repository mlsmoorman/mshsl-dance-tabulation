from django.urls import path
from .views.home_dashboard import kct_home
from .views.division_selector import division_selector
from .views.dashboard import kct_dashboard
from .views.entry import kct_entry
from .views.save_kct import save_kct
from .views.dangerous_move import report_dangerous_move


app_name = "kct"

urlpatterns = [
    path("", kct_home, name="home"), 
    path("<int:meet_id>/", division_selector, name="division_selector"), 
    path("<int:meet_id>/<str:division>/", kct_dashboard, name="kct_dashboard"), 
    path("entry/<int:entry_id>/", kct_entry, name="kct_entry"),
    path("entry/<int:entry_id>/save/", save_kct, name="save_kct"),
    path("entry/<int:entry_id>/dangerous/", report_dangerous_move, name="report_dangerous_move"),
]
