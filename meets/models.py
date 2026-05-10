from django.db import models
from core.models import School, User


##### DIVISION MODEL #####
class Division(models.TextChoices):
    JAZZ = "JAZZ", "Jazz"
    KICK = "KICK", "Kick"
    

##### CLASS LEVEL MODEL #####
class ClassLevel(models.TextChoices):
    A = "A", "A"
    AA = "AA", "AA"
    AAA = "AAA", "AAA",
    CONF = "CONF", "Conference"


##### MEET MODEL #####
class Meet(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    site = models.CharField(max_length=255)
    class_level = models.CharField(max_length=10, choices=ClassLevel.choices)
    division = models.CharField(max_length=10, choices=Division.choices)
    
    judges = models.ManyToManyField(User, related_name="judged_meets")
    kcts = models.ManyToManyField(User, related_name="kct_meets")
    
    def __str__(self):
        return f"{self.name} ({self.date})"

##### TEAM MODEL #####
class TeamEntry(models.Model):
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE, related_name="teams")
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    performance_order = models.PositiveBigIntegerField()
    verified_by_tabulator = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.school} @ ({self.meet})"
    