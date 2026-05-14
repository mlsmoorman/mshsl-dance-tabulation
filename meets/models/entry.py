from django.db import models
from core.models import School, Team, User
from .meet import Meet
from .choices import Division


#~.~.~.~.~.~.~.~.~.~.~.~.~ TEAM ENTRY ~.~.~.~.~.~.~.~.~.~.~.~.~#
class TeamEntry(models.Model):
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    division = models.CharField(max_length=10, choices=Division.choices)

    performance_order = models.PositiveSmallIntegerField()

    prelim_rank = models.IntegerField(null=True, blank=True)
    final_rank = models.IntegerField(null=True, blank=True)
    placement = models.IntegerField(null=True, blank=True)

    final_placement = models.IntegerField(null=True, blank=True)
    final_rank_points = models.IntegerField(null=True, blank=True)
    final_total_score = models.FloatField(null=True, blank=True)

    verified_by_tabulator = models.BooleanField(default=False)
    is_finalist = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.team} – {self.get_division_display()} @ {self.meet}"