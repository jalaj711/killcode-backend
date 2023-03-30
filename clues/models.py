from django.db import models

# Create your models here.
class Round(models.Model):
    number = models.IntegerField("Round Number", default=1)
    name = models.CharField("Round Name", default=1)
    start_time = models.DateTimeField("Start time of the round")
    end_time = models.DateTimeField("End time of the round")
    victim = models.ForeignKey(verbose_name="Victim in this round", on_delete=models.PROTECT)
    location = models.ForeignKey(verbose_name="Location of this round", on_delete=models.PROTECT)
    first_correct_team = models.ForeignKey(verbose_name="The first user to answer the question", default=None, on_delete=models.PROTECT)