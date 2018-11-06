from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from lookup.models import Country, City, Sport, SportIcon

User = get_user_model()


class CountrySerializer(ModelSerializer):
    class Meta:

        model = Country
        fields = '__all__'


class CitySerializer(ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    class Meta:

        model = City
        fields = ('name', 'country')

    def get_country(self, obj):
        return str(obj.country.name)


class CityOnlySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name', 'country')


class SportListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = ('id', 'name', 'description')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Sport.objects.all(),
                fields=('name', 'name'),
                message="Sport already exist"
            ), ]


class SportIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportIcon
        fields = ('id', 'sport', 'image')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Sport.objects.all(),
                fields=('sport', 'sport'),
                message="Icon for this sport already exist"
            ), ]


class SportDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = SportIconSerializer(source='sport_images', many=True)

    class Meta:
        model = Sport
        fields = ('id', 'name', 'description', 'image')

