from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=35)
    icon = models.ImageField(upload_to='country/images/')

    def save(self, *args, **kwargs):
        self.name = self.name[0].upper() + self.name[1:].lower()
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return str(str(self.pk) + ' ' + self.name)


class City(models.Model):
    name = models.CharField(max_length=35)
    country = models.ForeignKey(to=Country, related_name='country_id', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("name", "country"),)

    # def __iter__(self):
    #     return [self.name,
    #             self.pk]
    def __str__(self):
        return self.name


class Sport(models.Model):
    name = models.CharField(blank=True, unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sport_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='sport_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class SportIcon(models.Model):
    sport = models.ForeignKey(to=Sport, null=True, blank=True, related_name='sport_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sport/icons/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sport_image_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='sport_image_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)

