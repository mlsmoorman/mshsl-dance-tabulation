from django.contrib import admin
from .models import Meet, TeamEntry

#####  Registering Models  #####
@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "site", "class_level", "division")
    list_filter = ("class_level", "division", "date")
    search_fields = ("name", "site")
    filter_horizontal = ("judges", "kcts")
    
@admin.register(TeamEntry)
class TeamEntryAdmin(admin.ModelAdmin):
    list_display = ("school", "meet", "performance_order", "num_competitors")
    list_filters = ("meet", "school")
    search_fields = ("school__name")
    ordering = ("meet", "performance_order")
    
    