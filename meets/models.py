from django.db import models
from core.models import School, Team, User


##### DIVISION ENUM #####
class Division(models.TextChoices):
    JAZZ = "JAZZ", "Jazz"
    KICK = "KICK", "Kick"


##### CLASS LEVEL ENUM #####
class ClassLevel(models.TextChoices):
    A = "A", "A"
    AA = "AA", "AA"
    AAA = "AAA", "AAA"
    CONF = "CONF", "Conference"


##### MEET MODEL #####
class Meet(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    site = models.CharField(max_length=255)

    class_level = models.CharField(max_length=10, choices=ClassLevel.choices)
    num_finalists = models.IntegerField(default=6)

    judges = models.ManyToManyField(User, related_name="judged_meets")
    kcts = models.ManyToManyField(User, related_name="kct_meets")

    def __str__(self):
        return f"{self.name} ({self.date})"


##### TEAM ENTRY MODEL #####
class TeamEntry(models.Model):
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    division = models.CharField(max_length=10, choices=Division.choices)

    performance_order = models.PositiveSmallIntegerField()

    prelim_rank = models.IntegerField(null=True, blank=True)
    final_rank = models.IntegerField(null=True, blank=True)
    placement = models.IntegerField(null=True, blank=True)

    verified_by_tabulator = models.BooleanField(default=False)
    is_finalist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team} – {self.get_division_display()} @ {self.meet}"
