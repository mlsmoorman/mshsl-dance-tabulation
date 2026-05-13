from django.db import models
from django.contrib.auth.models import AbstractUser


##### TEAM LEVEL ENUM #####
class TeamLevel(models.TextChoices):
    VARSITY = "VARSITY", "Varsity"
    JV = "JV", "Junior Varsity"
    BSQUAD = "BSQUAD", "B-Squad"


##### SCHOOL MODEL #####
class School(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True)
    mascot = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


##### TEAM MODEL #####
class Team(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=TeamLevel.choices)

    def __str__(self):
        return f"{self.school.name} {self.name} ({self.get_level_display()})"


##### ROLE MODEL #####
class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


##### USER MODEL #####
class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)

    def has_role(self, code):
        return self.roles.filter(code=code).exists()


#~.~.~.~.~.~.~.~.~.~.~.~.~ RULES SET ~.~.~.~.~.~.~.~.~.~.~.~.~#
class RuleSet(models.Model):
    name = models.CharField(max_length=100, default="Default Rule Set")
    active = models.BooleanField(default=True)

    # Timing rules (seconds)
    jazz_min_time = models.IntegerField(default=120)   # 2:00
    jazz_max_time = models.IntegerField(default=150)  # 2:30
    kick_min_time = models.IntegerField(default=135)   # 2:15
    kick_max_time = models.IntegerField(default=165)  # 2:45

    # Kick count rules
    kick_min_count = models.IntegerField(default=35)
    kick_max_count = models.IntegerField(default=55)

    # Competitor count rules (Varsity only)
    varsity_min_competitors = models.IntegerField(default=5)
    varsity_jazz_max_competitors = models.IntegerField(default=26)
    varsity_kick_max_competitors = models.IntegerField(default=34)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Active: {self.active})"


#~.~.~.~.~.~.~.~.~.~.~.~.~  ~.~.~.~.~.~.~.~.~.~.~.~.~#