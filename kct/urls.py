from django.urls import path
from .views import kct_entry

urlpatterns = [
    path("entry/<int:entry_id>/kct/", kct_entry, name="kct_entry"),
]
