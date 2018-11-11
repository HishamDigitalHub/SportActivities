from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.template.defaultfilters import length

from rest_framework.fields import CurrentUserDefault

from rest_framework import serializers

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueTogetherValidator

from UserRegistrationApp.serializers import UserUpdateSerializer
from lookup.models import City, Country

from FitnessApp.models import Workout, Fitness, ExerciseVideo, ExerciseRating, Exercise, ExerciseImage, ExerciseIcon

User = get_user_model()


# #######  START IMAGES SERIALIZERS ######## #

class ExerciseImageCreateSerializer(serializers.HyperlinkedModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())

    class Meta:
        model = ExerciseImage
        fields = ('id', 'exercise', 'image',)


class ExerciseImageSerializer(serializers.HyperlinkedModelSerializer):
    # activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    class Meta:
        model = ExerciseImage
        fields = ('id', 'image',)

# #######  END IMAGES SERIALIZERS ######## #


# #######  START VIDEOS SERIALIZERS ######## #

class ExerciseVideoCreateSerializer(serializers.HyperlinkedModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())

    class Meta:
        model = ExerciseVideo
        fields = ('id', 'exercise', 'video',)


class ExerciseVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseVideo
        fields = ('id', 'video',)


# #######  END VIDEOS SERIALIZERS ######## #

# #######  START ICON SERIALIZERS ######## #

class ExerciseIconCreateSerializer(serializers.HyperlinkedModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())

    class Meta:
        model = ExerciseIcon
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ExerciseIcon.objects.all(),
                fields=('exercise', 'exercise'),
                message="You already sent an invitation request"
            ),
            ]
        fields = ('id', 'exercise', 'image',)


class ExerciseIconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseIcon
        fields = ('id', 'image',)


# #######  END ICON SERIALIZERS ######## #


# #######  END WORKOUT SERIALIZERS ######## #

# admin
# appointment
# #######  END WORKOUT SERIALIZERS ######## #
