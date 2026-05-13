from django.db import models

#~.~.~.~.~.~.~.~.~.~.~.~.~ DIVISION ENUM ~.~.~.~.~.~.~.~.~.~.~.~.~#
class Division(models.TextChoices):
    JAZZ = "JAZZ", "Jazz"
    KICK = "KICK", "Kick"


#~.~.~.~.~.~.~.~.~.~.~.~.~ CLASS LEVEL ENUM ~.~.~.~.~.~.~.~.~.~.~.~.~#
class ClassLevel(models.TextChoices):
    A = "A", "A"
    AA = "AA", "AA"
    AAA = "AAA", "AAA"
    CONF = "CONF", "Conference"