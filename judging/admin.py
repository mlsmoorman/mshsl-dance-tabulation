from django.contrib import admin
from .models import JudgeScoreSheet, KCTEntry

#####  Registering Models  #####
@admin.register(JudgeScoreSheet)
class JudgeScoreSheetAdmin(admin.ModelAdmin):
    list_display = (
		"team_entry",
		"judge",
		"division",
		"total",
		"rank",
	)
    list_filter = ("division", "judge", "team_entry__meet")
    search_fields = ("team_entry__school__name", "judge__username")
    readonly_fields = ("subtotal", "total")
    
@admin.register(KCTEntry)
class KCTEntryAdmin(admin.ModelAdmin):
    list_display = (
		"team_entry",
		"kct",
		"routine_time_seconds",
		"kick_count",
		"falls_observed",
		"dangerous_move_observed",
	)
    list_filter = ("team_entry__meet", "kct")
    search_fields = ("team_entry__school__name",)
    
    