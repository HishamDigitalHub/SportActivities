import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Avg
from lookup.models import Country, City, Sport


# Create your models here.


class Venue(models.Model):
    DAYS_CHOICES = (('sun', 'Sunday'), ('mon', 'monday'),
                    ('tue', 'Tuesday'), ('wed', 'Wednesday'),
                    ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'))

    name = models.CharField(blank=True, unique=True, max_length=100)
    admin = models.ForeignKey(User, null=True, blank=True, related_name='venueadmin', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, blank=True, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, blank=True, on_delete=models.DO_NOTHING)
    longitude = models.FloatField(blank=True, null=True, max_length=20)
    latitude = models.FloatField(blank=True, null=True, max_length=20)
    rating_average = models.FloatField(blank=True, null=True, default=0)
    hours_from = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    hours_to = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    days_open_from = models.CharField(blank=True, null=True, max_length=3, choices=DAYS_CHOICES)
    days_open_to = models.CharField(blank=True, null=True, max_length=3, choices=DAYS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='venue_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='venue_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(str(self.pk) + ' ' + self.name)


class VenueRating(models.Model):
    venue = models.ForeignKey(Venue, related_name='venue', on_delete=models.CASCADE, blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True, default=0)
    public_ind = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='venue_rate_user', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='venue_rate_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(VenueRating, self).save()
        rating = VenueRating.objects.filter(venue=self.venue).aggregate(Avg('rate'))['rate__avg']
        venue = self.venue
        venue_main = Venue.objects.get(id=venue.pk)
        venue_main.rating_average = rating
        venue_main.save()
        return rating


class VenueImage(models.Model):
    venue = models.ForeignKey(to=Venue, null=True, blank=True, related_name='venueimages',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='venue/images/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    profile_img_ind = models.BooleanField(default=False)
    cover_img_ind = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='venue_image_by_user', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='venue_image_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class VenueVideo(models.Model):
    venue = models.ForeignKey(to=Venue, null=True, blank=True, related_name='venuevideos',
                              on_delete=models.CASCADE)
    video = models.FileField(upload_to='venue/videos/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='venue_video_by_user', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='venue_video_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class VenuePreference(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))

    venue = models.OneToOneField(Venue, null=True, related_name='venue_activity', on_delete=models.CASCADE)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    sport = models.ManyToManyField(Sport, related_name='activity_preference_sport', blank=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='venue_preference_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='venue_preference_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

