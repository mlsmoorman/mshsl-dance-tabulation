from django.db import models
from core.models import User
from meets.models import TeamEntry, Division

#~.~.~.~.~.~.~.~.~.~.~.~.~ JUDGE SCORE SHEET MODEL ~.~.~.~.~.~.~.~.~.~.~.~.~#
class JudgeScoreSheet(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team_entry = models.ForeignKey(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="score_sheets"
    )

    # Remove division field — always use team_entry.division
    @property
    def division(self):
        return self.team_entry.division

    ## Jazz Skills
    skills_turns = models.PositiveSmallIntegerField(null=True, blank=True)
    skills_leaps_jumps = models.PositiveSmallIntegerField(null=True, blank=True)

    ## Kick Skills
    kicks_technique = models.PositiveSmallIntegerField(null=True, blank=True)
    kicks_height = models.PositiveSmallIntegerField(null=True, blank=True)

    ## Shared Categories
    choreo_creativity = models.PositiveSmallIntegerField()
    choreo_visual_effect = models.PositiveSmallIntegerField()
    diff_routine = models.PositiveSmallIntegerField()
    diff_formations = models.PositiveSmallIntegerField()
    diff_skills_or_kicks = models.PositiveSmallIntegerField()
    exec_placement_control = models.PositiveSmallIntegerField()
    exec_accuracy = models.PositiveSmallIntegerField()
    routine_effectiveness = models.PositiveSmallIntegerField()

    ## Deductions
    time_deduction = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    kick_deduction = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    other_deduction = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    ## Computed
    subtotal = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    total = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    rank = models.PositiveSmallIntegerField(null=True, blank=True)

    def compute_subtotal(self):
        fields = [
            "choreo_creativity",
            "choreo_visual_effect",
            "diff_routine",
            "diff_formations",
            "diff_skills_or_kicks",
            "exec_placement_control",
            "exec_accuracy",
            "routine_effectiveness",
        ]

        if self.division == Division.JAZZ:
            fields += ["skills_turns", "skills_leaps_jumps"]
        else:
            fields += ["kicks_technique", "kicks_height"]

        self.subtotal = sum(getattr(self, f) or 0 for f in fields)

    def compute_total(self):
        self.compute_subtotal()
        self.total = self.subtotal - (
            self.time_deduction + self.kick_deduction + self.other_deduction
        )

    def save(self, *args, **kwargs):
        self.compute_total()
        super().save(*args, **kwargs)

#~.~.~.~.~.~.~.~.~.~.~.~.~ ISSUES MODEL ~.~.~.~.~.~.~.~.~.~.~.~.~#
class IssueType(models.TextChoices):
    TIME = "TIME", "Timing Violation"
    KICK = "KICK", "Kick Count Issue"
    COMPETITOR = "COMPETITOR", "Competitor Count Issue"
    SAFETY = "SAFETY", "Safety / Illegal Skill"
    COMMENT = "COMMENT", "Judge Comment Flag"
    SCORE_OUTLIER = "SCORE_OUTLIER", "Score Outlier"
    MISSING_SHEET = "MISSING_SHEET", "Missing Judge Sheet"
    MANUAL = "MANUAL", "Manual Issue"

class Issue(models.Model):
    team_entry = models.ForeignKey(
        TeamEntry,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    flagged_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    issue_type = models.CharField(max_length=50, choices=IssueType.choices)
    message = models.TextField(blank=True)

    auto_generated = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_issue_type_display()} – {self.team_entry}"
