from django.urls import path
from . import views

app_name = "meets"

urlpatterns = [
    path("meet/<int:pk>/tabulator/", views.tabulator_dashboard, name="tabulator_dashboard"),
]

