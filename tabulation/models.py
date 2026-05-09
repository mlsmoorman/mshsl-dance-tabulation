from django.db import models
from meets.models import TeamEntry

#####  SCORESHEET RANKING MODEL  #####
class RankSystem(models.TextChoices):
    A = "A", "Rank A (7-8 judges)"
    B = "B", "Rank B (5-6 judges)"
    C = "C", "Rank C (4 or fewer judges)"
    
class TeamResult(models.Model):
    team_entry = models.OneToOneField(TeamEntry, on_delete=models.CASCADE, related_name="result")
    rank_system = models.CharField(max_length=1, choices=RankSystem.choices)
    
    ranks_list = models.CharField(max_length=1, choices=RankSystem.choices)
    dropped_ranks = models.JSONField(default=list)
    
    rank_total = models.PositiveIntegerField()
    final_place = models.PositiveIntegerField(null=True, blank=True)
    
    disqualified = models.BooleanField(default=False)
