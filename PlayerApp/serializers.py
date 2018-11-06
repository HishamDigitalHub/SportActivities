from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.fields import CurrentUserDefault

from rest_framework import serializers

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from UserRegistrationApp.serializers import UserUpdateSerializer
from lookup.models import City, Country

from PlayerApp.models import PlayerImage, PlayerVideo

User = get_user_model()

# #######  START IMAGES SERIALIZERS ######## #


class PlayerImageCreateSerializer(serializers.HyperlinkedModelSerializer):
   # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PlayerImage
        fields = ('image',)


class PlayerImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerImage
        fields = ('image',)

# #######  END IMAGES SERIALIZERS ######## #

# #######  START VIDEOS SERIALIZERS ######## #


class PlayerVideoCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PlayerVideo
        fields = ('user', 'video',)


class PlayerVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerVideo
        fields = ('video',)

# #######  END VIDEOS SERIALIZERS ######## #
