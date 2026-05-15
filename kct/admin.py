from django.contrib import admin
from .models import KCTEntry

@admin.register(KCTEntry)
class KCTEntryAdmin(admin.ModelAdmin):
    list_display = [
        "team_entry",
        "num_competitors",
        "routine_time_seconds",
        "kick_count",
        "jazz_team_turn_performed",
        "jazz_leap_jump_performed",
        "falls_observed",
        "dangerous_move_observed",
    ]

    list_filter = [
        "jazz_team_turn_performed",
        "jazz_leap_jump_performed",
        "dangerous_move_observed",
    ]

    search_fields = [
        "team_entry__team__name",
        "team_entry__division",
    ]
