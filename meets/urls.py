from django.urls import path
from . import views

app_name = "meets"

urlpatterns = [
    path("meet/<int:pk>/tabulator/", views.tabulator_dashboard, name="tabulator_dashboard"),
]

urlpatterns += [
    path("entry/<int:entry_id>/verify/", views.verify_entry, name="verify_entry"),
    path("meet/<int:pk>/finalize/", views.finalize_meet, name="finalize_meet"),
    path("meet/<int:pk>/select-finalists/", views.select_finalists, name="select_finalists"),
]

