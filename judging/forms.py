from django import forms
from .models import JudgeScoreSheet
from meets.models import Division


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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sheet = self.instance
        if sheet.division == Division.JAZZ:
            self.fields["kicks_technique"].widget = forms.HiddenInput()
            self.fields["kicks_height"].widget = forms.HiddenInput()
        else:
            self.fields["skills_turns"].widget = forms.HiddenInput()
            self.fields["skills_leaps_jumps"].widget = forms.HiddenInput()
