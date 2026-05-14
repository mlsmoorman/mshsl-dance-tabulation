from django import forms
from .models import JudgeScoreSheet
from meets.models.entry import Division


class JudgeScoreSheetForm(forms.ModelForm):
    class Meta:
        model = JudgeScoreSheet
        fields = [
            "skills_turns",
            "skills_leaps_jumps",
            "kicks_technique",
            "kicks_height",
            "choreo_creativity",
            "choreo_visual_effect",
            "diff_routine",
            "diff_formations",
            "diff_skills_or_kicks",
            "exec_placement_control",
            "exec_accuracy",
            "routine_effectiveness",
            "time_deduction",
            "kick_deduction",
            "other_deduction",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        self.team_entry = kwargs.pop("team_entry")
        super().__init__(*args, **kwargs)

    def _validate_1_to_10(self, field_name, required=True):
        value = self.cleaned_data.get(field_name)
        if value is None:
            if required:
                self.add_error(field_name, "This field is required.")
            return
        if not (1 <= value <= 10):
            self.add_error(field_name, "Score must be between 1 and 10.")

    def clean(self):
        cleaned = super().clean()
        division = self.team_entry.division

        # Shared categories (always required, 1–10)
        shared_fields = [
            "choreo_creativity",
            "choreo_visual_effect",
            "diff_routine",
            "diff_formations",
            "diff_skills_or_kicks",
            "exec_placement_control",
            "exec_accuracy",
            "routine_effectiveness",
        ]
        for f in shared_fields:
            self._validate_1_to_10(f, required=True)

        # Division‑specific skills
        if division == Division.JAZZ:
            self._validate_1_to_10("skills_turns", required=True)
            self._validate_1_to_10("skills_leaps_jumps", required=True)
            # Kick fields optional/ignored
        else:
            self._validate_1_to_10("kicks_technique", required=True)
            self._validate_1_to_10("kicks_height", required=True)
            # Jazz skill fields optional/ignored

        return cleaned
