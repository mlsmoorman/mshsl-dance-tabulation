from django.contrib import admin
from .models import User, School
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#####  Registering Models  #####

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
		("Role", {"fields": ("role",)}),
	)
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation")
    search_fields = ("name", "abbreviation")
    
