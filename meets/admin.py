from django.contrib import admin
from .models import Meet, TeamEntry
from core.models import User
from judging.admin import JudgeScoreSheetInline
from kct.admin import KCTEntryInline
from deductions.models import RoutineDeduction

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
    

class RoutineDeductionsInline(admin.TabularInline):
    model = RoutineDeduction
    extra = 0
    readonly_fields = ("entered_by", "timestamp")

    def has_add_permission(self, request, obj=None):
        return request.user.roles.filter(name="Superior Judge").exists()

    def has_change_permission(self, request, obj=None):
        return request.user.roles.filter(name="Superior Judge").exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.roles.filter(name="Superior Judge").exists()


@admin.register(TeamEntry)
class TeamEntryAdmin(admin.ModelAdmin):
    list_display = ("team", "meet", "performance_order")
    list_filter = ("meet", "team")
    search_fields = ("team__name",)
    ordering = ("meet", "performance_order")

    inlines = [
        KCTEntryInline,
        JudgeScoreSheetInline,
        RoutineDeductionsInline,
    ]
