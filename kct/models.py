from django.db import models
from core.models import User
from meets.models.entry import TeamEntry


class KCTEntry(models.Model):
    team_entry = models.ForeignKey(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="kct_entries"
    )
    kct = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="kct_entries"
    )

    num_competitors = models.PositiveIntegerField()
    routine_time_seconds = models.PositiveIntegerField()
    kick_count = models.PositiveIntegerField(null=True, blank=True)

    jazz_team_turn_performed = models.BooleanField(default=True)
    jazz_team_leap_jump_performed = models.BooleanField(default=True)

    falls_observed = models.BooleanField(default=False)
    dangerous_move_observed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team_entry", "kct")

    def __str__(self):
        return f"KCT Entry for {self.team_entry} by {self.kct}"

    # Helper: get the other KCT entry
    def get_other_kct_entry(self):
        return (
            KCTEntry.objects
            .filter(team_entry=self.team_entry)
            .exclude(id=self.id)
            .first()
        )
