from django.urls import path
from .views.setup import meet_setup
from .views.team import add_team
from .views.entry import add_entry
from .views.edit_entry import edit_entry


urlpatterns = [
    path("setup/", meet_setup, name="meet_setup"),
    path("add-team/", add_team, name="add_team"),
    path("add-entry/<int:meet_id>/<int:team_id>/", add_entry, name="add_entry"),
    path("edit-entry/<int:entry_id>/", edit_entry, name="edit_entry"),
]
