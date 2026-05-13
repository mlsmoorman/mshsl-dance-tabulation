from django.contrib import admin
from .models import JudgeScoreSheet


@admin.register(JudgeScoreSheet)
class JudgeScoreSheetAdmin(admin.ModelAdmin):
    list_display = (
        "judge",
        "team_entry",
        "division",
        "subtotal",
        "total",
        "rank",
    )
    list_filter = ("division", "judge", "team_entry__meet")
    search_fields = ("judge__username", "team_entry__team__school__name")
