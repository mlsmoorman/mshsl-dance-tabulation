from django.db import models
from meets.models.entry import TeamEntry

class KCTEntry(models.Model):
    team_entry = models.OneToOneField(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="kct_entries"
    )

    # Which KCT submitted this entry (1, 2, or more)
    kct_number = models.PositiveSmallIntegerField()

    num_competitors = models.PositiveIntegerField(null=True, blank=True)
    
    # Timing
    routine_time_seconds = models.PositiveSmallIntegerField(null=True, blank=True)

    # Kick Count
    kick_count = models.PositiveSmallIntegerField(null=True, blank=True)

    # Jazz Skills
    jazz_team_turn_performed = models.BooleanField(default=False)
    jazz_leap_jump_performed = models.BooleanField(default=False)

    # Observations
    falls_observed = models.BooleanField(default=False)
    dangerous_move_observed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("team_entry", "kct_number")

    def __str__(self):
        return f"KCT Entry for {self.team_entry}"


