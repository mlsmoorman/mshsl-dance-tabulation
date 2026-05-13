from django import forms
from .models import KCTEntry


class KCTEntryForm(forms.ModelForm):
    class Meta:
        model = KCTEntry
        fields = [
            "num_competitors",
            "routine_time_seconds",
            "kick_count",
            "jazz_team_turn_performed",
            "jazz_team_leap_jump_performed",
            "falls_observed",
            "dangerous_move_observed",
        ]

    def __init__(self, *args, **kwargs):
        self.team_entry = kwargs.pop("team_entry")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        division = self.team_entry.division

        # Kick division → kick_count required
        if division == "KICK":
            if cleaned.get("kick_count") is None:
                self.add_error("kick_count", "Kick count is required for Kick routines.")

        # Jazz division → kick_count optional, but >5 is a warning
        if division == "JAZZ":
            kc = cleaned.get("kick_count")
            if kc is not None and kc > 5:
                self.add_error("kick_count", "Jazz routines should not exceed 5 kicks.")

        # Jazz turn/leap required
        if division == "JAZZ":
            if not cleaned.get("jazz_team_turn_performed"):
                self.add_error("jazz_team_turn_performed", "Jazz turn must be performed.")
            if not cleaned.get("jazz_team_leap_jump_performed"):
                self.add_error("jazz_team_leap_jump_performed", "Jazz leap/jump must be performed.")

        # Competitor count minimums
        if cleaned.get("num_competitors") < 5:
            self.add_error("num_competitors", "Minimum of 5 competitors required.")

        return cleaned
