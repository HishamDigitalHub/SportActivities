from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

from django.db.models import Avg

from VenueApp.models import Venue
from lookup.models import Sport
# Create your models here.


class Workout(models.Model):
    admin = models.ForeignKey(User, null=True, blank=True, related_name='workout_admin', on_delete=models.CASCADE)
    appointment = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='workout_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='workout_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class Fitness(models.Model):
    workout = models.ForeignKey(to=Workout, null=True, related_name='fitness_workout', blank=True,
                                on_delete=models.DO_NOTHING)
    heart_rate_average = models.FloatField(blank=True, null=True, default=0)
    heart_rate_max = models.FloatField(blank=True, null=True, default=0)
    heart_rate_min = models.FloatField(blank=True, null=True, default=0)
    duration = models.IntegerField(blank=True, null=True, default=0)
    burned_calories = models.FloatField(blank=True, null=True, default=0)
    appointment = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='fitness_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='fitness_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        self.heart_rate_average = (self.heart_rate_max + self.heart_rate_min) / 2
        super().save(*args, **kwargs)


class Exercise(models.Model):
    workout = models.ForeignKey(to=Workout, null=True, related_name='exercise_workout', blank=True,
                                on_delete=models.DO_NOTHING)
    sport = models.ForeignKey(Sport, null=True, blank=True, related_name='exercise_sport', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    freq_planned = models.IntegerField(blank=True, null=True, default=1)
    freq_played = models.IntegerField(blank=True, null=True)
    measurement = models.CharField(max_length=50, blank=True, null=True)
    admin = models.ForeignKey(User, null=True, blank=True, related_name='exercise_admin', on_delete=models.CASCADE)
    appointment = models.DateTimeField(blank=True, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.DO_NOTHING, related_name='exercise_venue')
    rating_average = models.FloatField(blank=True, null=True, default=0)
    public_ind = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='exercise_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='exercise_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class ExerciseIcon(models.Model):
    exercise = models.ForeignKey(to=Exercise, null=True, blank=True, related_name='icon_exercise', on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='exercise/icons/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='exercise_icon_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='exercise_icon_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class ExerciseRating(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='exercise_rate', on_delete=models.CASCADE, blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True, default=0)
    created_by = models.ForeignKey(User, related_name='exercise_rate_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='exercise_rate_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ExerciseRating, self).save()
        rating = ExerciseRating.objects.filter(exercise=self.exercise).aggregate(Avg('rate'))['rate__avg']
        exercise = self.exercise
        exercise_main = Exercise.objects.get(id=exercise.pk)
        exercise_main.rating_average = rating
        exercise_main.save()
        return rating


class ExerciseImage(models.Model):
    exercise = models.ForeignKey(to=Exercise, null=True, blank=True, related_name='exercise_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='exercise/images/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    profile_img_ind = models.BooleanField(default=False)
    cover_img_ind = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='exercise_image_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='exercise_image_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class ExerciseVideo(models.Model):
    exercise = models.ForeignKey(to=Exercise, on_delete=models.CASCADE, related_name='exercise_videos', blank=True, null=True)
    video = models.FileField(upload_to='exercise/videos/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='exercise_video_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='exercise_video_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


# class HeartBeat(models.Model):
#     minimum = models.IntegerField(blank=True, null=True, default=0)
#     maximum = models.IntegerField(blank=True, null=True, default=0)
#     # Type = models.
#     icon = models.ImageField(upload_to='health/heart_beat/', null=True, blank=True)
#     fitness = models.ForeignKey(Fitness, related_name='fitness_heart_beat', blank=True, null=True, on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, related_name='heart_beat_created_by', blank=True, null=True,
#                                    on_delete=models.DO_NOTHING)
#     updated_date = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(to=User, null=True, related_name='heart_beat_updated_by', blank=True,
#                                    on_delete=models.DO_NOTHING)


