from django.db import models
from decimal import Decimal

from meets.models import TeamEntry
from core.models import User


class DeductionType(models.Model):
    PENALTY_TYPES = [
        ("DQ", "Disqualification"),
        ("POINT", "Point Deduction"),
        ("WARNING", "Warning"),
    ]

    DIVISIONS = [
        ("JAZZ", "Jazz"),
        ("KICK", "High Kick"),
        ("BOTH", "Both"),
    ]

    code = models.CharField(max_length=50, unique=True)
    rule_reference = models.CharField(max_length=100)
    description = models.TextField()

    division = models.CharField(max_length=10, choices=DIVISIONS, default="BOTH")
    penalty_type = models.CharField(max_length=20, choices=PENALTY_TYPES)

    points = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    max_points = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    per_occurrence = models.BooleanField(default=False)
    per_judge = models.BooleanField(default=False)
    minor_or_flagrant = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} — {self.rule_reference}"


class RoutineDeduction(models.Model):
    team_entry = models.ForeignKey(
        TeamEntry, on_delete=models.CASCADE, related_name="deductions"
    )
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)

    entered_by = models.ForeignKey(User, on_delete=models.PROTECT)

    count = models.PositiveIntegerField(default=1)
    judges_reporting = models.PositiveIntegerField(default=1)

    minor = models.BooleanField(default=False)
    flagrant = models.BooleanField(default=False)

    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team_entry} — {self.deduction_type.code}"

    def compute_points_for_one_judge(self) -> Decimal:
        rule = self.deduction_type

        if rule.penalty_type != "POINT":
            return Decimal("0.0")

        if rule.points is None:
            return Decimal("0.0")

        pts = Decimal(rule.points)

        if rule.per_occurrence:
            pts *= self.count

        if rule.max_points is not None:
            pts = min(pts, Decimal(rule.max_points))

        return pts
