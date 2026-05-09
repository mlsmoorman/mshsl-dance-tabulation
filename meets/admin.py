from django.contrib import admin
from .models import Meet, TeamEntry
from core.models import User
from judging.admin import KCTEntryInline, JudgeScoreSheetInline

@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "site", "class_level", "division")
    list_filter = ("class_level", "division", "date")
    search_fields = ("name", "site")
    filter_horizontal = ("judges", "kcts")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "judges":
            kwargs["queryset"] = User.objects.filter(roles__name="Judge")
        if db_field.name == "kcts":
            kwargs["queryset"] = User.objects.filter(roles__name="KCT")
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(TeamEntry)
class TeamEntryAdmin(admin.ModelAdmin):
    list_display = ("school", "meet", "performance_order")
    list_filter = ("meet", "school")
    search_fields = ("school__name",)
    ordering = ("meet", "performance_order")

    inlines = [
        KCTEntryInline,
        JudgeScoreSheetInline,
    ]

    