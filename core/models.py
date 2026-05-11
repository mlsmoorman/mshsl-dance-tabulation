from django.db import models
from django.contrib.auth.models import AbstractUser

#####  • A user can now have any combination of roles
#####  • Roles are stored in a separate table
#####  • You can add more roles later (Coach, Admin, Coordinator, etc.)

class Role(models.Model):
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)   # e.g. "JUDGE", "KCT", "TABULATOR", "SUPERIOR_JUDGE"
    name = models.CharField(max_length=100)               # Human readable

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name="users", blank=True)


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Team(models.Model):
    LEVELS = [
        ("Varsity", "Varsity"),
        ("JV", "Junior Varsity"),
        ("B-Squad", "B-Squad"),
    ]
    
    name = models.CharField(max_length=255)     #Team/School Name
    level = models.CharField(max_length=50, choices=LEVELS, null=True, blank=True)     #Varsity, JV, B-Squad
    
    def __str__(self):
        return self.name