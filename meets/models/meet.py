from django.db import models
from core.models import School, Team, User
from .choices import ClassLevel


class Meet(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    site = models.CharField(max_length=255)

    class_level = models.CharField(max_length=10, choices=ClassLevel.choices)
    num_finalists = models.IntegerField(default=6)

    judges = models.ManyToManyField(User, related_name="judged_meets")
    kcts = models.ManyToManyField(User, related_name="kct_meets")

#    disqualified = models.BooleanField(default=False)
    dq_reason = models.TextField(blank=True, null=True)
    dq_timestamp = models.DateTimeField(blank=True, null=True)
    dq_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="dq_actions"
    )

    ruleset = models.ForeignKey(
        "meets.RuleSet",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    
    locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    locked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} ({self.date})"
    
    