from django.db import models
from core.models import User
from meets.models import TeamEntry


#####  KICK COUNTER/TIMER MODEL  #####
class KCTEntry(models.Model):
    team_entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE, related_name="kct_entries")
    kct = models.ForeignKey(User, on_delete=models.CASCADE)
    
    num_competitors = models.PositiveIntegerField()
    routine_time_seconds = models.PositiveIntegerField()
    kick_count = models.PositiveIntegerField(null=True, blank=True)
    
    jazz_team_turn_performed = models.BooleanField(default=True)
    jazz_team_leap_jump_performed = models.BooleanField(default=True)
    
    falls_observed = models.BooleanField(default=False)
    dangerous_move_observed = models.BooleanField(default=False)
    