# meets.models.ruleset.py
from django.db import models

class RuleSet(models.Model):
    name = models.CharField(max_length=100, default="Default Rule Set")
    active = models.BooleanField(default=True)

    # Timing rules (seconds)
    jazz_min_time = models.IntegerField(default=120)   # 2:00
    jazz_max_time = models.IntegerField(default=150)   # 2:30
    kick_min_time = models.IntegerField(default=135)   # 2:15
    kick_max_time = models.IntegerField(default=165)   # 2:45

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
