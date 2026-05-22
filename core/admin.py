from django.contrib import admin
from .models import School, Team, Role, User, RuleSet
from meets.models.entry import TeamEntry


#~.~.~.~.~.~.~.~.~.~.~.~.~ RULES ADMIN ~.~.~.~.~.~.~.~.~.~.~.~.~#
@admin.register(RuleSet)
class RuleSetAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "updated_at")
    list_editable = ("active",)


#~.~.~.~.~.~.~.~.~.~.~.~.~ SCHOOL ADMIN ~.~.~.~.~.~.~.~.~.~.~.~.~#
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "mascot")
    search_fields = ("name", "city")


#~.~.~.~.~.~.~.~.~.~.~.~.~ TEAM ADMIN ~.~.~.~.~.~.~.~.~.~.~.~.~#
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("school", "name", "level")
    list_filter = ("level", "school")
    search_fields = ("school__name", "name")


#~.~.~.~.~.~.~.~.~.~.~.~.~ ROLE ADMIN ~.~.~.~.~.~.~.~.~.~.~.~.~#
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


#~.~.~.~.~.~.~.~.~.~.~.~.~ USER ADMIN ~.~.~.~.~.~.~.~.~.~.~.~.~#
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name")
    filter_horizontal = ("roles",)
    search_fields = ["username", "first_name", "last_name", "email"]


#~.~.~.~.~.~.~.~.~.~.~.~.~ TEAM ENTRY ADMIN ~.~.~.~.~.~.~.~.~.~.~.~.~#
@admin.register(TeamEntry)
class TeamEntryAdmin(admin.ModelAdmin):
    list_display = ("meet", "team", "division", "performance_order")
    list_filter = ("meet", "division")
    search_fields = ("team__name",)


#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#

