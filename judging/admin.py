from django import forms 
from django.contrib import admin
from .models import JudgeScoreSheet, KCTEntry
from .scoring import ScoringEngine
from .forms import TimeMMSSField

##  Anytime a scoresheet is saved (admin or in app):
##  • Subtotal and total are recomputed,
##  • Kick deductions are pulled from KCT,
##  • Time deductions can be automated later.

class JudgeScoreSheetInline(admin.TabularInline):
    model = JudgeScoreSheet
    extra = 0
    readonly_fields = ("subtotal", "total", "rank")
    fields = (
        "judge",
        "division",
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
        "subtotal",
        "total",
        "rank",
    )

@admin.register(JudgeScoreSheet)
class JudgeScoreSheetAdmin(admin.ModelAdmin):
    list_display = ("team_entry", "judge", "division", "total", "rank")
    list_filter = ("division", "judge", "team_entry__meet")
    search_fields = ("team_entry__school__name", "judge__username")
    readonly_fields = ("subtotal", "total")

    def save_model(self, request, obj, form, change):
        ScoringEngine.apply_to_scoresheet(obj)
        super().save_model(request, obj, form, change)
        
        
        
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

