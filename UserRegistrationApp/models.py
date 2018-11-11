from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from TeamApp.models import Team
from lookup.models import Country, City, Sport


# Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    TYPE_CHOICES = (('P', 'Player'), ('T', 'Trainer'), ('B', 'Both'))

    user = models.OneToOneField(User, related_name='origin_user', on_delete=models.CASCADE)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    mobile_no = models.CharField(blank=True, max_length=15)
    longitude = models.FloatField(blank=True, null=True, max_length=20)
    latitude = models.FloatField(blank=True, null=True, max_length=20)
    DOB = models.DateField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    facebook_id = models.TextField(blank=True, null=True)
    google_id = models.TextField(blank=True, null=True)
    public_profile_ind = models.BooleanField(default=True)
    follow_profile_ind = models.BooleanField(default=True)
    type = models.CharField(blank=True, null=True, max_length=1, choices=TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, related_name='profile_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='profile_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def __str__(self):
        full_name = str(self.pk) + ' ' + self.user.first_name + ' ' + self.user.last_name
        return full_name

    # email = models.CharField(max_length=100, blank=False)
    # first_name = models.CharField(max_length=100, blank=False)
    # last_name = models.CharField(max_length=100, blank=False)
    # password = models.CharField(max_length=100, blank=False)


class UserPreference(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))

    user = models.OneToOneField(User, null=True, related_name='preference_user', on_delete=models.CASCADE)
    max_distance = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    sport = models.ManyToManyField(Sport, blank=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_preference_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='user_preference_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

# to create and saved and updated with user model
# #################################################


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
