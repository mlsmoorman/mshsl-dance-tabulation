from django.db import models
from django.utils import timezone

from meets.models.meet import Meet
from meets.models.entry import TeamEntry
from core.models import User


from django.db import models

class DeductionType(models.Model):
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=128)
    points = models.DecimalField(max_digits=4, decimal_places=1)
    per_occurrence = models.BooleanField(default=True)
    applies_to_jazz = models.BooleanField(default=True)
    applies_to_kick = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.points})"


# -------------------------------------------------------------
# FINAL RESULTS SNAPSHOT
# Stores the final ranking + scores after tabulation is locked.
# -------------------------------------------------------------
class FinalResult(models.Model):
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE)

    final_rank = models.IntegerField()
    final_placement = models.IntegerField()
    final_rank_points = models.IntegerField()
    final_total_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["final_rank"]

    def __str__(self):
        return f"{self.entry.team.name} – Rank {self.final_rank}"


# -------------------------------------------------------------
# VERIFICATION LOG
# Records when a tabulator verifies an entry’s scores.
# -------------------------------------------------------------
class VerificationLog(models.Model):
    entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verified {self.entry} at {self.verified_at}"


# -------------------------------------------------------------
# MEET LOCK
# Records when a meet is locked by the tabulator.
# -------------------------------------------------------------
class MeetLock(models.Model):
    meet = models.OneToOneField(Meet, on_delete=models.CASCADE)
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    locked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.meet.name} locked at {self.locked_at}"
