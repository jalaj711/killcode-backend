from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(models.Model):
    name = models.CharField("Name of the team", max_length=50, unique=True)
    points = models.IntegerField("Current Score of the Team", default=0)

# Create your models here.
class TeamMember(AbstractUser):
    name = models.CharField("Name Of the Team Member", max_length=100)
    email = models.CharField("Email of the team member", max_length=150, unique=True)
    phone_number = models.CharField("Phone Number of the team member", max_length=25)
    team = models.ForeignKey(Team, verbose_name="Team of the user", on_delete=models.PROTECT, null=True)
