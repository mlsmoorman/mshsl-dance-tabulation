from django.db import models
from .choices import Division, ClassLevel
from core.models import TeamLevel
from .meet import Meet

class Team(models.Model):
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=255, blank=True, null=True)

    level = models.CharField(
        max_length=10,
        choices=TeamLevel.choices,
        default=TeamLevel.VARSITY
    )

    division = models.CharField(
        max_length=10,
        choices=Division.choices,
        default=Division.JAZZ
    )

    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()} – {self.get_division_display()})"
