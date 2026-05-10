from django.contrib import admin
from .models import DeductionType, RoutineDeduction


@admin.register(DeductionType)
class DeductionTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "rule_reference", "penalty_type", "division")
    search_fields = ("code", "rule_reference", "description")
    list_filter = ("penalty_type", "division")


@admin.register(RoutineDeduction)
class RoutineDeductionAdmin(admin.ModelAdmin):
    list_display = (
        "team_entry",
        "deduction_type",
        "entered_by",
        "count",
        "judges_reporting",
        "minor",
        "flagrant",
        "timestamp",
    )
    list_filter = ("deduction_type__penalty_type", "entered_by")
    search_fields = ("team_entry__id", "team_entry__school__name", "deduction_type__code")

    def has_add_permission(self, request):
        return request.user.roles.filter(name="Superior Judge").exists()

    def has_change_permission(self, request, obj=None):
        if request.user.roles.filter(name="Tabulator").exists():
            return False
        return request.user.roles.filter(name="Superior Judge").exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.roles.filter(name="Superior Judge").exists()
