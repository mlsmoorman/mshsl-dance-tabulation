from django.contrib import admin
from .models import JudgeScoreSheet


@admin.register(JudgeScoreSheet)
class JudgeScoreSheetAdmin(admin.ModelAdmin):
    list_display = (
        "team_entry",
        "judge",
        "total",
        "rank",
    )
    list_filter = ("judge",)
