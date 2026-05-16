from django.db import models
from meets.models.entry import TeamEntry


class DeductionType(models.Model):
    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=128)
    points = models.DecimalField(max_digits=4, decimal_places=1)
    per_occurrence = models.BooleanField(default=True)
    applies_to_jazz = models.BooleanField(default=True)
    applies_to_kick = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.points})"


class RoutineDeduction(models.Model):
    team_entry = models.ForeignKey(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="routine_deductions"
    )
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    def total_points(self):
        return self.count * self.deduction_type.points

    def __str__(self):
        return f"{self.deduction_type.label} x{self.count}"
