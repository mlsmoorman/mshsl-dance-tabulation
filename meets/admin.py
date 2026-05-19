from django.contrib import admin
from .models.entry import Meet, TeamEntry
from .models.assignments import JudgeAssignment, KCTAssignment

class JudgeAssignmentInline(admin.TabularInline):
    model = JudgeAssignment
    extra = 0
    ordering = ("judge_number",)
    fields = ("judge_number", "judge")
    autocomplete_fields = ("judge",)


class KCTAssignmentInline(admin.TabularInline):
    model = KCTAssignment
    extra = 0
    ordering = ("kct_number",)
    fields = ("kct_number", "kct")
    autocomplete_fields = ("kct",)


@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "site", "class_level", "locked")
    list_filter = ("class_level", "locked")
    search_fields = ("name", "site")

    inlines = [
        JudgeAssignmentInline,
        KCTAssignmentInline,
    ]

# Replaced below on 5.18.26
#class TeamEntryInline(admin.TabularInline):
#    model = TeamEntry
#    extra = 0
#
#
#@admin.register(Meet)
#class MeetAdmin(admin.ModelAdmin):
#    list_display = ("name", "date", "site", "class_level")
#    list_filter = ("class_level", "date")
#    search_fields = ("name", "site")
#    inlines = [TeamEntryInline]
#
#
#@admin.register(TeamEntry)
#class TeamEntryAdmin(admin.ModelAdmin):
#    list_display = (
#        "meet",
#        "team",
#        "division",
#        "performance_order",
#        "prelim_rank",
#        "final_rank",
#        "placement",
#        "verified_by_tabulator",
#        "is_finalist",
#    )
#    list_filter = ("division", "meet")
#    search_fields = ("team__school__name", "team__name", "meet__name")
