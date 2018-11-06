from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Avg

from VenueApp.models import Venue
from lookup.models import Country, City, Sport


# Create your models here.


class Activity(models.Model):
    admin = models.ForeignKey(User, null=True, blank=True, related_name='activityadmin', on_delete=models.CASCADE)
    name = models.CharField(blank=True, unique=True, max_length=100)
    longitude = models.FloatField(blank=True, null=True, max_length=20)
    latitude = models.FloatField(blank=True, null=True, max_length=20)
    rating_average = models.FloatField(blank=True, null=True, default=0)
    country = models.ForeignKey(Country, blank=True, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, blank=True, on_delete=models.DO_NOTHING)
    number_of_players = models.IntegerField(blank=True, null=True, default=0)
    players = models.ManyToManyField(User, blank=True, related_name='activityplayers')
    appointment = models.DateTimeField(blank=True, null=True)
    public_ind = models.BooleanField(default=True)
    venue = models.ForeignKey(Venue, blank=True, on_delete=models.DO_NOTHING, default=12)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


    # def __str__(self):
    #     return str(str(self.pk) + ' ' + self.name)


class ActivityRating(models.Model):
    activity = models.ForeignKey(Activity, related_name='activity', on_delete=models.CASCADE, blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True, default=0)
    created_by = models.ForeignKey(User, related_name='rate_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='rate_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ActivityRating, self).save()
        rating = ActivityRating.objects.filter(activity=self.activity).aggregate(Avg('rate'))['rate__avg']
        activity = self.activity
        activity_main = Activity.objects.get(id=activity.pk)
        activity_main.rating_average = rating
        activity_main.save()
        return rating


class ActivityInvite(models.Model):
    STATUS_CHOICES = (('P', 'Pending'), ('A', 'Accepted'),
                      ('R', 'Rejected'), ('K', 'Kicked'),
                      ('L', 'Left'), ('C', 'Cancel'))

    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='activity_from_user', blank=True,
                                  null=True)
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='activity_to_user', blank=True,
                                null=True)
    date_time = models.DateTimeField(default=datetime.now)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='invite_to_activity', blank=True,
                                 null=True)
    status = models.CharField(blank=True, null=True, max_length=1, choices=STATUS_CHOICES)
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='activity_invite_by_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='activity_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class ActivityImage(models.Model):
    activity = models.ForeignKey(to=Activity, null=True, blank=True, related_name='activityimages',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='activity/images/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='activity_image_by_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='activity_image_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class ActivityVideo(models.Model):
    activity = models.ForeignKey(to=Activity, null=True, blank=True, related_name='activityvideos',
                                 on_delete=models.CASCADE)
    video = models.FileField(upload_to='activity/videos/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='activity_video_by_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='activity_video_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class ActivityPreference(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))

    activity = models.OneToOneField(Activity, null=True, related_name='preference_activity', on_delete=models.CASCADE)
    max_distance = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    sport = models.ManyToManyField(Sport, blank=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='activity_preference_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='activity_preference_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)
