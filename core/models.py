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
