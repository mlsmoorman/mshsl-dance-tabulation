from django.db import models
from django.utils import timezone
from core.models import User
from meets.models.entry import TeamEntry
from tabulation.models import DeductionType


class IssueType(models.TextChoices):
    FALL = "FALL", "Fall"
    DANGEROUS_MOVE = "DANGEROUS_MOVE", "Dangerous Move"
    ILLEGAL_SKILL = "ILLEGAL_SKILL", "Illegal Skill"
    SAFETY = "SAFETY", "Safety"
    TIME = "TIME", "Time Violation"
    KICK = "KICK", "Kick Count Violation"
    COMPETITOR = "COMPETITOR", "Competitor Count"
    OTHER = "OTHER", "Other"

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


class IssueSeverity(models.TextChoices):
    WARNING = "WARNING", "Warning"
    POTENTIAL_DEDUCTION = "POTENTIAL_DEDUCTION", "Potential Deduction"
    DEDUCTION = "DEDUCTION", "Deduction"


class IssueStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    RESOLVED = "RESOLVED", "Resolved"


class Issue(models.Model):
    team_entry = models.ForeignKey(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_issues",
    )
    issue_type = models.CharField(max_length=32, choices=IssueType.choices)
    severity = models.CharField(
        max_length=32,
        choices=IssueSeverity.choices,
        default=IssueSeverity.POTENTIAL_DEDUCTION,
    )
    status = models.CharField(
        max_length=16,
        choices=IssueStatus.choices,
        default=IssueStatus.OPEN,
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Resolution
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_issues",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_action = models.CharField(
        max_length=32,
        blank=True,
        help_text="APPLY_DEDUCTION / WARNING_ONLY / NO_ACTION",
    )
    resolution_notes = models.TextField(blank=True)

    def resolve(self, user, action, notes=""):
        self.status = IssueStatus.RESOLVED
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolution_action = action
        self.resolution_notes = notes
        self.save()

    def __str__(self):
        return f"{self.issue_type} — {self.team_entry}"


class DQStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    REJECTED = "REJECTED", "Rejected"


class DQReason(models.TextChoices):
    DANGEROUS_MOVE = "DANGEROUS_MOVE", "Dangerous Move"
    ILLEGAL_SKILL = "ILLEGAL_SKILL", "Illegal Skill"
    SAFETY = "SAFETY", "Safety"
    OTHER = "OTHER", "Other"


class DQEntry(models.Model):
    team_entry = models.ForeignKey(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="dq_entries",
    )
    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reported_dqs",
    )
    reason = models.CharField(max_length=32, choices=DQReason.choices)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=16,
        choices=DQStatus.choices,
        default=DQStatus.PENDING,
    )
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="confirmed_dqs",
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def confirm(self, user):
        self.status = DQStatus.CONFIRMED
        self.confirmed_by = user
        self.confirmed_at = timezone.now()
        self.save()

    def reject(self, user):
        self.status = DQStatus.REJECTED
        self.confirmed_by = user
        self.confirmed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"DQ — {self.team_entry} ({self.status})"
