from django.contrib import admin
from .models import JudgeScoreSheet

@admin.register(JudgeScoreSheet)
class JudgeScoreSheetAdmin(admin.ModelAdmin):
    list_display = ["judge", "team_entry", "total", "rank"]
