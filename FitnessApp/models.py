from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

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
    heart_rate_average = models.FloatField(blank=True, null=True, default=0)
    heart_rate_max = models.FloatField(blank=True, null=True, default=0)
    heart_rate_min = models.FloatField(blank=True, null=True, default=0)
    # duration = models. ..
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



#
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


