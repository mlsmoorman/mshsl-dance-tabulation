# deductions/models.py

from django.db import models
from meets.models import TeamEntry
from core.models import User
from .models import DeductionType

class RoutineDeduction(models.Model):
    team_entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE, related_name="deductions")
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)

    # Who entered it — must be Superior Judge
    entered_by = models.ForeignKey(User, on_delete=models.PROTECT)

    count = models.PositiveIntegerField(default=1)
    judges_reporting = models.PositiveIntegerField(default=1)

    minor = models.BooleanField(default=False)
    flagrant = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team_entry} — {self.deduction_type.code}"
