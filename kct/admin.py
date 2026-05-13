from django.contrib import admin
from .models import KCTEntry


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


@admin.register(KCTEntry)
class KCTEntryAdmin(admin.ModelAdmin):
    list_display = (
        "team_entry",
        "kct",
        "num_competitors",
        "routine_time_seconds",
        "kick_count",
        "falls_observed",
        "dangerous_move_observed",
    )
    list_filter = ("kct", "dangerous_move_observed", "falls_observed")

