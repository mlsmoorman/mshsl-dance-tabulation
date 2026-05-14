from django import forms
from .models import Issue, DQEntry


class IssueResolutionForm(forms.ModelForm):
    resolution_action = forms.ChoiceField(
        choices=[
            ("APPLY_DEDUCTION", "Apply Deduction"),
            ("WARNING_ONLY", "Warning Only"),
            ("NO_ACTION", "No Action"),
        ]
    )

    class Meta:
        model = Issue
        fields = ["resolution_action", "resolution_notes"]


class DQEntryForm(forms.ModelForm):
    class Meta:
        model = DQEntry
        fields = ["reason", "notes"]
