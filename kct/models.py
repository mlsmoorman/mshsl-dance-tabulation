from django.db import models
from meets.models.entry import TeamEntry

class KCTEntry(models.Model):
    team_entry = models.OneToOneField(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="kct_entry"
    )

    num_competitors = models.PositiveIntegerField(null=True, blank=True)
    
    # Timing
    routine_time_seconds = models.PositiveSmallIntegerField(null=True, blank=True)

    # Kick Count
    kick_count = models.PositiveSmallIntegerField(null=True, blank=True)

    # Jazz Skills
    jazz_team_turn_performed = models.BooleanField(default=False)
    jazz_leap_jump_performed = models.BooleanField(default=False)

    # Observations
    falls_observed = models.PositiveSmallIntegerField(default=0)
    dangerous_move_observed = models.BooleanField(default=False)

    def __str__(self):
        return f"KCT Entry for {self.team_entry}"
