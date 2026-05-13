from django.contrib import admin
from .models import School, Team, Role, User, TeamLevel


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "mascot")
    search_fields = ("name", "city")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("school", "name", "level")
    list_filter = ("level", "school")
    search_fields = ("school__name", "name")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name")
    filter_horizontal = ("roles",)
