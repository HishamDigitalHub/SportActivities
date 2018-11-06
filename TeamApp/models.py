from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


from lookup.models import Country, City, Sport


# Create your models here.


class Team(models.Model):

    admin = models.ForeignKey(User, null=True, blank=True, related_name='admin', on_delete=models.CASCADE)
    name = models.CharField(blank=True, unique=True, max_length=100)
    longitude = models.FloatField(blank=True, null=True, max_length=20)
    latitude = models.FloatField(blank=True, null=True, max_length=20)
    score = models.IntegerField(blank=True, null=True, default=0)
    country = models.ForeignKey(Country, blank=True, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, blank=True, on_delete=models.DO_NOTHING)
    players = models.ManyToManyField(User, blank=True, related_name='players')
    public_ind = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='team_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='team_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    # def __str__(self):
    #     return str(str(self.pk) + ' ' + self.name)


class TeamImage(models.Model):
    team = models.ForeignKey(to=Team, null=True, blank=True, related_name='teamimages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='team/images/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    profile_img_ind = models.BooleanField(default=False)
    cover_img_ind = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='team_image_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='team_image_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class TeamVideo(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name='teamvideos', blank=True, null=True)
    video = models.FileField(upload_to='team/videos/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='team_video_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='team_video_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class TeamInvite(models.Model):
    STATUS_CHOICES = (('P', 'Pending'), ('A', 'Accepted'),
                      ('R', 'Rejected'), ('K', 'Kicked'),
                      ('L', 'Left'), ('C', 'Cancel'))

    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='invite_by', blank=True, null=True)
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='invite_to', blank=True, null=True)
    date_time = models.DateTimeField(default=datetime.now)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invite_to_team', blank=True, null=True)
    status = models.CharField(blank=True, null=True, max_length=1, choices=STATUS_CHOICES)
    active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='team_invite_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='team_invite_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class TeamPreference(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))

    team = models.OneToOneField(Team, null=True, related_name='preference_team', on_delete=models.CASCADE)
    max_distance = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    sport = models.ManyToManyField(Sport, blank=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='team_preference_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='team_preference_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)
