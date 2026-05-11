from django import forms 
from django.contrib import admin
from kct.models import KCTEntry
from .forms import TimeMMSSField

class KCTEntryForm(forms.ModelForm):
    routine_time_seconds = TimeMMSSField()

    class Meta:
        model = KCTEntry
        fields = "__all__"


@admin.register(KCTEntry)
class KCTEntryAdmin(admin.ModelAdmin):
    form = KCTEntryForm

    list_display = (
        "team_entry",
        "kct",
        "num_competitors",
        "routine_time_seconds",
        "kick_count",
        "falls_observed",
        "dangerous_move_observed",
    )
    list_filter = ("team_entry__meet", "kct")
    search_fields = ("team_entry__school__name",)
    

class KCTEntryInline(admin.TabularInline):
    model = KCTEntry
    extra = 1
    fields = (
        "kct",
        "num_competitors",
        "routine_time_seconds",
        "kick_count",
        "jazz_team_turn_performed",
        "jazz_team_leap_jump_performed",
        "falls_observed",
        "dangerous_move_observed",
    )

