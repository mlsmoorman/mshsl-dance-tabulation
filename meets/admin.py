from django.contrib import admin
from .models.entry import Meet, TeamEntry


class TeamEntryInline(admin.TabularInline):
    model = TeamEntry
    extra = 0


@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "site", "class_level")
    list_filter = ("class_level", "date")
    search_fields = ("name", "site")
    inlines = [TeamEntryInline]


@admin.register(TeamEntry)
class TeamEntryAdmin(admin.ModelAdmin):
    list_display = (
        "meet",
        "team",
        "division",
        "performance_order",
        "prelim_rank",
        "final_rank",
        "placement",
        "verified_by_tabulator",
        "is_finalist",
    )
    list_filter = ("division", "meet")
    search_fields = ("team__school__name", "team__name", "meet__name")
