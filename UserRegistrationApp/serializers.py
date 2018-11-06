from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from .models import Profile, UserPreference
from lookup.models import Country, City, Sport
from lookup.serializers import (CountrySerializer, CitySerializer, SportDetailSerializer, SportIconSerializer)

User = get_user_model()


# ######### START USER SERIALIZER ##########

# 11111111111111111111111111111111111111111
class UserCreateSerializer(ModelSerializer):
    # Used in ProfileCreateSerializer
    class Meta:
        model = User
        fields = [
            # 'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]


# 22222222222222222222222222222222222222222
class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name'
        ]


# ######### END USER SERIALIZERS ###########


# ######### START PROFILE SERIALIZERS ##########

# 3333333333333333333333333333333333333333333
class ProfileUpdateSerializer(ModelSerializer):
    user = UserUpdateSerializer(required=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('user',
                  'mobile_no',
                  'longitude',
                  'latitude',
                  'DOB',
                  'height',
                  'weight',
                  'facebook_id',
                  'google_id',
                  'public_profile_ind',
                  'follow_profile_ind',
                  'type',
                  )


# Done Completely
# 44444444444444444444444444444444444444444444
class ProfileListSerializer(ModelSerializer):

    user = SerializerMethodField()
    first_name = SerializerMethodField()
    last_name = SerializerMethodField()
    email = SerializerMethodField()
    country = SerializerMethodField()
    city = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'first_name',
                  'last_name',
                  'gender',
                  'email',
                  'mobile_no',
                  'country',
                  'city',
                  'longitude',
                  'latitude',
                  'DOB',
                  'height',
                  'weight',
                  'facebook_id',
                  'google_id',
                  'public_profile_ind',
                  'follow_profile_ind',
                  'type',)

    def get_user(self, obj):
        return str(obj.user.username)

    def get_first_name(self, obj):
        return str(obj.user.first_name)

    def get_last_name(self, obj):
        return str(obj.user.last_name)

    def get_email(self, obj):
        return str(obj.user.email)

    def get_country(self, obj):
        return str(obj.country.name)

    def get_city(self, obj):
        return str(obj.city.name)


# 55555555555555555555555555555555555555555555555

class ProfileDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    first_name = SerializerMethodField()
    last_name = SerializerMethodField()
    email = SerializerMethodField()
    country = SerializerMethodField()
    city = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'first_name',
                  'last_name',
                  'email',
                  'gender',
                  'mobile_no',
                  'country',
                  'city',
                  'longitude',
                  'latitude',
                  'DOB',
                  'height',
                  'weight',
                  'facebook_id',
                  'google_id',
                  'public_profile_ind',
                  'follow_profile_ind',
                  'type',)

    def get_user(self, obj):
        return str(obj.user.username)

    def get_first_name(self, obj):
        return str(obj.user.first_name)

    def get_last_name(self, obj):
        return str(obj.user.last_name)

    def get_email(self, obj):
        return str(obj.user.email)

    def get_country(self, obj):
        return str(obj.country.name)

    def get_city(self, obj):
        return str(obj.city.name)


# 6666666666666666666666666666666666666666666

# ############################################
class PreferenceCreateSerializer(ModelSerializer):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))
    user_name = SerializerMethodField()
    country_name = SerializerMethodField()
    city_name = SerializerMethodField()
    sport_name = SerializerMethodField()

    class Meta:

        model = UserPreference
        fields = (
            'id',
            'user',
            'user_name',
            'max_distance',
            'country',
            'country_name',
            'city',
            'city_name',
            'gender',
            'sport',
            'sport_name',
            'min_age',
            'max_age',
        )

    def get_country_name(self, obj):
        return str(obj.country.name)

    def get_city_name(self, obj):
        return str(obj.city.name)

    def get_sport_name(self, obj):
        sports = obj.sport.all()  # values('id','name')

        if sports:
            from django.core import serializers
            import ast
            sport_name = serializers.serialize("json", sports)
            sport_name = ast.literal_eval(sport_name)
            # new_list = []
            # for i in range(len(sport_name)):
            #
            #     new_list.append(sport_name[i]["fields"]["name"])
            # sport_name = new_list
            keys = ['id', 'name']
            array_length = len(sport_name)
            sport_list = []

            for i in range(array_length):
                sport_dict = {}
                sport_dict.update({keys[0]: (sport_name[i]["pk"]), keys[1]: (sport_name[i]["fields"]["name"])})
                dummy_dict = sport_dict
                sport_list.append(dummy_dict)

            # sport_name = x
            return sport_list

    def get_user_name(self, obj):
        return str(str(obj.user.first_name) + ' ' + str(obj.user.last_name))


class ProfileCreateSerializer(ModelSerializer):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

    user = UserCreateSerializer(required=True)
    # country = CountrySerializer(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    # gender = serializers.CharField(source='get_gender_display')
    mobile_no = serializers.CharField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    # gender = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.CharField()
    DOB = serializers.DateField()
    height = serializers.IntegerField()
    weight = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ('user',
                  'gender',
                  'mobile_no',
                  'longitude',
                  'latitude',
                  'DOB',
                  'country',
                  'city',
                  'height',
                  'weight',
                  'facebook_id',
                  'google_id',
                  'type',
                  )
        extra_kwargs = {'mobile_no': {'required': True},
                        'gender': {'required': True},
                        'longitude': {'required': True},
                        'latitude': {'required': True},
                        'DOB': {'required': True},
                        'country': {'required': True},
                        'city': {'required': True},
                        'height': {'required': True},
                        'weight': {'required': True}}

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """

        user_data = validated_data.pop('user')
        user = UserCreateSerializer.create(UserCreateSerializer(), validated_data=user_data)
        user.set_password(user.password)
        user.save()

        profile, created = Profile.objects.update_or_create(
            user=user,
            # user_id=validated_data.pop('user_id'),
            country=validated_data.pop('country'),
            gender=validated_data.pop('gender'),
            city=validated_data.pop('city'),
            mobile_no=validated_data.pop('mobile_no'),
            longitude=validated_data.pop('longitude'),
            latitude=validated_data.pop('latitude'),
            DOB=validated_data.pop('DOB'),
            height=validated_data.pop('height'),
            weight=validated_data.pop('weight'),
            facebook_id=validated_data.pop('facebook_id'),
            google_id=validated_data.pop('google_id')
        )

        return profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id',
                  'mobile_no',
                  'longitude',
                  'latitude',
                  'DOB',
                  'height',
                  'weight',
                  'facebook_id',
                  'google_id',
                  'public_profile_ind',
                  'follow_profile_ind',
                  'type',)


#
# class UserSerializer(serializers.ModelSerializer):
#     mobile_no = ProfileSerializer(many=True) # (source='Profile')
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'mobile_no')
#
#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile')
#         # Unless the application properly enforces that this field is
#         # always set, the follow could raise a `DoesNotExist`, which
#         # would need to be handled.
#         profile = instance.profile
#
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()
#
#         profile.is_premium_member = profile_data.get(
#             'is_premium_member',
#             profile.is_premium_member
#         )
#         profile.has_support_contract = profile_data.get(
#             'has_support_contract',
#             profile.has_support_contract
#         )
#         profile.save()
#
#         return instance
#

# # run and work fine for user >> first name , last name , email

class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        """
        Override update method because we need to update
        nested serializer for profile
        """
        if validated_data.get('profile', ):
            profile_data = validated_data.get('profile', )
            profile_serializer = ProfileSerializer(data=profile_data)

            if profile_serializer.is_valid():
                profile = profile_serializer.update(instance=instance.profile)
                validated_data['profile'] = profile

        return super(UserSerializer, self).update(instance, validated_data)
