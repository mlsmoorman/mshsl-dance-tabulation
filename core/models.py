from django.db import models
from django.contrib.auth.models import AbstractUser

#####  USER MODEL - SELECTS USER WHICH DETERMINES VIEW  #####
class User(AbstractUser):
    ROLE_CHOICES = [
		("JUDGE", "Judge"),
		("KCT", "Kick Counter/Timer"),
		("TABULATOR", "Tabulator"),
		("COACH", "Coach"),
		("ADMIN", "Admin"),
	]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

#####  SCHOOL MODEL - SELECTS SCHOOL  #####
class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.name

