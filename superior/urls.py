from django.urls import path
from .views import dashboard, review, issue_actions, dq_actions

app_name = "superior"

urlpatterns = [
    path("meet/<int:meet_id>/", dashboard.superior_dashboard, name="dashboard"),
    path("review/<int:entry_id>/", review.superior_review, name="review"),
    path("issue/<int:issue_id>/resolve/", issue_actions.resolve_issue, name="resolve_issue"),
    path("dq/<int:entry_id>/create/", dq_actions.create_dq, name="create_dq"),
    path("dq/<int:dq_id>/confirm/", dq_actions.confirm_dq, name="confirm_dq"),
    path("dq/<int:dq_id>/reject/", dq_actions.reject_dq, name="reject_dq"),
]
