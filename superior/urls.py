from django.urls import path
from .views import dashboard, review, dq_actions, remove_deduction
from .views.issues_dashboard import superior_issues_dashboard
from .views.resolve_issues import resolve_issue

app_name = "superior"

urlpatterns = [
    path("meet/<int:meet_id>/", dashboard.superior_dashboard, name="dashboard"),
    path("review/<int:entry_id>/", review.superior_review, name="review"),
    path("dq/<int:entry_id>/create/", dq_actions.create_dq, name="create_dq"),
    path("dq/<int:dq_id>/confirm/", dq_actions.confirm_dq, name="confirm_dq"),
    path("dq/<int:dq_id>/reject/", dq_actions.reject_dq, name="reject_dq"),
    path("meet/<int:meet_id>/issues/", superior_issues_dashboard, name="issues_dashboard"),
    path("issue/<int:issue_id>/resolve/", resolve_issue, name="resolve_issue"),
    path("remove_deduction/<int:deduction_id>/", remove_deduction, name="remove_deduction"),
]
