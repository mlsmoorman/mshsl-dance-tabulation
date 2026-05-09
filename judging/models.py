from django.db import models
from core.models import User
from meets.models import TeamEntry, Division


#####  JUDGES' SCORESHEET MODEL  #####
class JudgeScoreSheet(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team_entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE, related_name="score_sheets")
    division = models.CharField(max_length=10, choices=Division.choices)
    
    ##  JAZZ Skills
    skills_turns = models.PositiveSmallIntegerField(null=True, blank=True)
    skills_leaps_jumps = models.PositiveSmallIntegerField(null=True, blank=True)
    
    ##  KICK Skills
    kicks_technique = models.PositiveSmallIntegerField(null=True, blank=True)
    kicks_height = models.PositiveSmallIntegerField(null=True, blank=True)
    
    
    #####  SHARED CATEGORIES  #####
    ##  CHOREOGRAPHY
    choreo_creativity = models.PositiveSmallIntegerField()
    choreo_visual_effect = models.PositiveSmallIntegerField()
    
    ##  DIFFICULTY
    diff_routine = models.PositiveSmallIntegerField()
    diff_formations = models.PositiveSmallIntegerField()
    diff_skills_or_kicks = models.PositiveSmallIntegerField()
    
    ##  EXECUTION
    exec_placement_control = models.PositiveSmallIntegerField()
    exec_accuracy = models.PositiveSmallIntegerField()
    
    ##  ROUTINE EFFECTIVENESS
    routine_effectiveness = models.PositiveSmallIntegerField()
    
    ##  Deductions (per Judge)
    time_deduction = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    kick_deduction = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    other_deduction = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    
    ##  Computed
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
    