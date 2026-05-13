from django import forms
import re

from .models import KCTEntry
from judging.models import Division
from judging.services.issue_detection import get_active_rules


 #~.~.~.~.~.~.~.~.~.~.~.~.~ TIME MMSS FIELD ~.~.~.~.~.~.~.~.~.~.~.~.~#
class TimeMMSSField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        
        # Accept only MM:SS 
        if not re.match(r"^\d{1,2}:\d{2}$", value):
            raise forms.ValidationError("Enter time as MM:SS")
        
        minutes, seconds = value.split(":")
        minutes = int(minutes)
        seconds = int(seconds)
        
        # Convert MM:SS to seconds for use in python calculations
        if seconds >= 60:
            raise forms.ValidationError("Seconds must be < 60")
        
        return minutes * 60 + seconds
    
	# Converts back to MM:SS for display purposes
    def prepare_value(self, value):
        if value is None:
            return ""
        minutes = value // 60
        seconds = value % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    
    
#~.~.~.~.~.~.~.~.~.~.~.~.~ KCT ENTRY FORM ~.~.~.~.~.~.~.~.~.~.~.~.~#
class KCTEntryForm(forms.ModelForm):
    class Meta:
        model = KCTEntry
        fields = [
            "actual_time_seconds",
            "kick_count",
            "turn_completed",
            "leap_completed",
            "competitor_count",
        ]
        widgets = {
            "actual_time_seconds": forms.NumberInput(attrs={"class": "form-control"}),
            "kick_count": forms.NumberInput(attrs={"class": "form-control"}),
            "competitor_count": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        entry = self.instance.entry
        rules = get_active_rules()

        time = cleaned.get("actual_time_seconds")
        kicks = cleaned.get("kick_count")
        competitors = cleaned.get("competitor_count")

        # Timing validation
        if entry.division == Division.JAZZ:
            if time and not (rules.jazz_min_time <= time <= rules.jazz_max_time):
                self.add_error("actual_time_seconds",
                    f"Jazz time must be between {rules.jazz_min_time} and {rules.jazz_max_time} seconds."
                )
        else:
            if time and not (rules.kick_min_time <= time <= rules.kick_max_time):
                self.add_error("actual_time_seconds",
                    f"Kick time must be between {rules.kick_min_time} and {rules.kick_max_time} seconds."
                )

        # Kick count validation
        if entry.division == Division.KICK:
            if kicks and not (rules.kick_min_count <= kicks <= rules.kick_max_count):
                self.add_error("kick_count",
                    f"Kick count must be between {rules.kick_min_count} and {rules.kick_max_count}."
                )

        # Competitor count validation (Varsity only)
        if entry.team.level == "Varsity":
            if competitors < rules.varsity_min_competitors:
                self.add_error("competitor_count",
                    f"Varsity teams must have at least {rules.varsity_min_competitors} competitors."
                )

            if entry.division == Division.JAZZ:
                if competitors > rules.varsity_jazz_max_competitors:
                    self.add_error("competitor_count",
                        f"Jazz Varsity max competitors is {rules.varsity_jazz_max_competitors}."
                    )
            else:
                if competitors > rules.varsity_kick_max_competitors:
                    self.add_error("competitor_count",
                        f"Kick Varsity max competitors is {rules.varsity_kick_max_competitors}."
                    )

        return cleaned


    #~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#