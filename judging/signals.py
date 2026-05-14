# judging/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JudgeScoreSheet
from superior.issue_factory import regenerate_issues_for_entry


@receiver(post_save, sender=JudgeScoreSheet)
def judge_score_sheet_post_save(sender, instance, **kwargs):
    team_entry = instance.team_entry
    regenerate_issues_for_entry(team_entry)
