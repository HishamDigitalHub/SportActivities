from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from datetime import date

from django.contrib.auth.models import User, UserManager


# Create your models here.


class UserExtension(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    longitude = models.FloatField()
    latitude = models.FloatField()
    DOB = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    facebook_id = models.TextField()
    google_id = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    # email = models.CharField(max_length=100, blank=False)
    # first_name = models.CharField(max_length=100, blank=False)
    # last_name = models.CharField(max_length=100, blank=False)
    # password = models.CharField(max_length=100, blank=False)


