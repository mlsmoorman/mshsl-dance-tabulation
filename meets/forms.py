from django import forms
from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from meets.models.ruleset import RuleSet
from meets.models.choices import Division
from core.models import Team

class MeetForm(forms.ModelForm):
    class Meta:
        model = Meet
        fields = ["name", "date", "site", "class_level", "num_finalists", "ruleset"]

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "school", "level"]

class TeamEntryForm(forms.ModelForm):
    class Meta:
        model = TeamEntry
        fields = ["division", "performance_order"]

class InlineTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "school", "level"]
