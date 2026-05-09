from django import forms
import re


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