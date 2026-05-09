from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name="users", blank=True)


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
#####  • A user can now have any combination of roles
#####  • Roles are stored in a separate table
#####  • You can add more roles later (Coach, Admin, Coordinator, etc.)