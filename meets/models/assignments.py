from django.db import models
from django.conf import settings
from .meet import Meet


# Judge Assignment
class JudgeAssignment(models.Model):
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    judge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    judge_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("meet", "judge_number")
        ordering = ["judge_number"]

    def __str__(self):
        return f"Judge {self.judge_number} — {self.judge}"

# KCT Assignment
class KCTAssignment(models.Model):
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    kct = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kct_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("meet", "kct_number")
        ordering = ["kct_number"]

    def __str__(self):
        return f"KCT {self.kct_number} — {self.kct}"