from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PlayerImage(models.Model):
    user = models.ForeignKey(to=User, null=True, blank=True, related_name='playerimages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/images/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    profile_img_ind = models.BooleanField(default=False)
    cover_img_ind = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='player_image_by_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='player_image_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)


class PlayerVideo(models.Model):
    user = models.ForeignKey(to=User, null=True, blank=True, related_name='playervideos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='user/videos/', null=True, blank=True)
    public_ind = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='player_video_by_user', blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, null=True, related_name='player_video_updated_by', blank=True,
                                   on_delete=models.DO_NOTHING)
