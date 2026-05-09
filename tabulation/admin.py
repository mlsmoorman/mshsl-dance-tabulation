from django.contrib import admin
from .models import TeamResult

@admin.register(TeamResult)
class TeamResultAdmin(admin.ModelAdmin):
    list_display = ("team_entry", "rank_system", "rank_total", "final_place", "disqualified")
    list_filter = ("rank_system", "disqualified")
    search_fields = ("team_entry__school__name",)
