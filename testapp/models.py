from django.db import models
from datetime import date

# Create your models here.


class Json1Test(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=190)
    subject = models.DateField(default=date.today)
    date = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)


