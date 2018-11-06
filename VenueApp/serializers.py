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

from VenueApp.models import VenueRating, VenueImage, Venue, VenueVideo, VenuePreference

User = get_user_model()


# #######  START IMAGES SERIALIZERS ######## #

class VenueImageCreateSerializer(serializers.HyperlinkedModelSerializer):
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = VenueImage
        fields = ('venue', 'image',)


class VenueImageSerializer(serializers.HyperlinkedModelSerializer):
    # venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())
    class Meta:
        model = VenueImage
        fields = ('image',)

# #######  END IMAGES SERIALIZERS ######## #


# #######  START VIDEOS SERIALIZERS ######## #

class VenueVideoCreateSerializer(serializers.HyperlinkedModelSerializer):
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = VenueVideo
        fields = ('venue', 'video',)


class VenueVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VenueVideo
        fields = ('video',)


# #######  END VIDEOS SERIALIZERS ######## #


# #######  START TEAMS SERIALIZERS ######## #

class VenueDetailsSerializer(ModelSerializer):
    images = VenueImageSerializer(source='venueimages', many=True)
    videos = VenueVideoSerializer(source='venuevideos', many=True)

    class Meta:
        model = Venue
        fields = [
            'admin',
            'id',
            'name',
            'longitude',
            'latitude',
            'rating_average',
            'country',
            'city',
            'hours_from',
            'hours_to',
            'days_open_from',
            'days_open_to',
            'images',
            'videos'
        ]


class MyVenueListSerializer(ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name']


class VenueCreateSerializer(ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'admin',
            'id',
            'name',
            'longitude',
            'latitude',
            'rating_average',
            'country',
            'city',
            'hours_from',
            'hours_to',
            'days_open_from',
            'days_open_to',
        ]

    def create(self, validated_data):
        obj = Venue.objects.create(**validated_data)
        # obj.players.add(obj.created_by)
        obj.save()
        return obj


class VenueRateSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     created_by = kwargs['context']['request'].user
    #     super(VenueRateSerializer, self).__init__(*args, **kwargs)
    #     self.fields['created_by'].queryset = User.objects.filter(id=created_by.id)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                    default=serializers.CurrentUserDefault())
    # venue = serializers.IntegerField()

    # venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    def validate(self, attrs):
        attrs = super(VenueRateSerializer, self).validate(attrs)  # calling default validation
        venue = attrs['venue']
        rate = attrs['rate']
        print(venue.id)
        print(attrs['venue'])
        already_rated = VenueRating.objects.filter(created_by=self.context['request'].user, venue=venue.id)
        if not Venue.objects.filter(id=venue.id):
            raise serializers.ValidationError("To rate, you should be a member in this venue")
        elif already_rated.exists():
            raise serializers.ValidationError("This user has already rated.")
        elif rate == 0:
            raise serializers.ValidationError("Can't rate 0, rate between 1-5")
        elif rate < 0:
            raise serializers.ValidationError("Cant rate less than 1")
        elif rate > 5:
            raise serializers.ValidationError("Can't rate greater than 5")
        return attrs

    class Meta:
        model = VenueRating
        fields = ['id', 'venue', 'rate', 'created_by']


# #######  END TEAMS SERIALIZERS ######## #


# ############################################
class VenuePreferenceCreateSerializer(ModelSerializer):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))
    venue_name = SerializerMethodField()
    # country_name = SerializerMethodField()
    # city_name = SerializerMethodField()
    sport_name = SerializerMethodField()

    class Meta:

        model = VenuePreference
        fields = (
            'id',
            'venue',
            'venue_name',
            # 'country',
            # 'country_name',
            # 'city',
            # 'city_name',
            'gender',
            'sport',
            'sport_name',
            'min_age',
            'max_age',
        )

    # def get_country_name(self, obj):
    #     return str(obj.country.name)
    #
    # def get_city_name(self, obj):
    #     return str(obj.city.name)

    def get_sport_name(self, obj):
        sports = obj.sport.all()  # values('id','name')

        if sports:
            from django.core import serializers
            import ast
            sport_name = serializers.serialize("json", sports)
            sport_name = ast.literal_eval(sport_name)
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

    def get_venue_name(self, obj):
        return str(obj.venue.name)

# #######  END PREFERENCE SERIALIZERS ######## #



# #######  START TEAM INVITES SERIALIZERS ######## #


# ### Start Venue
#
# class VenueInviteCreateSerializer(serializers.ModelSerializer):
#     venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())
#     from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     method_name = serializers.SerializerMethodField()
#
#     # serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())
#     # to_user =
#
#     def __init__(self, *args, **kwargs):
#         from_user = kwargs['context']['request'].user
#         # venue = kwargs['context']['request'].venue
#         super(VenueInviteCreateSerializer, self).__init__(*args, **kwargs)
#         self.fields['from_user'].queryset = User.objects.filter(id=from_user.id)
#         # status = "A"
#         # self.fields['status'].queryset = VenueInvite.objects.filter(status=status)
#
#         # self.fields['from_user'].queryset = Venue.objects.filter(players__in=from_user.id)
#
#     class Meta:
#         model = VenueInvite
#         fields = ('id', 'from_user', 'to_user', 'date_time', 'venue', 'method_name', 'status')
#
#         validators = [
#             serializers.UniqueTogetherValidator(
#                 queryset=VenueInvite.objects.filter(status="P", active=True),
#                 fields=('to_user', 'venue'),
#                 message="You already sent an invitation request"
#             ),
#             serializers.UniqueTogetherValidator(
#                 queryset=VenueInvite.objects.filter(status="A", active=True),
#                 fields=('to_user', 'venue'),
#                 message="this user already in the venue"
#             ),
#             serializers.UniqueTogetherValidator(
#                 queryset=VenueInvite.objects.filter(status="K", active=True),
#                 fields=('to_user', 'venue'),
#                 message="this user was kicked by admin of this venue"
#             ),
#         ]
#
#     def create(self, validated_data):
#         obj = VenueInvite.objects.create(**validated_data)
#         obj.status = "P"
#         obj.active = True
#         obj.save()
#         return obj
#
#     def get_method_name(self, *args, **kwargs):
#         method_name = None  # kwargs['context']['request'].method_name
#         return method_name
#
#
# class MyVenueInviteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VenueInvite
#         fields = ('id', 'from_user', 'date_time', 'venue', 'status')
#
#
# class VenueInviteAcceptDeclineSerializer(serializers.ModelSerializer):
#     method_name = serializers.CharField(write_only=True, default="")
#
#     class Meta:
#         model = VenueInvite
#         fields = ('id', 'from_user', 'to_user', 'venue', 'method_name', 'status')
#
#     def get_method_name(self, *args, **kwargs):
#         method_name = None  # kwargs['context']['request'].method_name
#         return method_name
#
#     def update(self, instance, validated_data):
#         method_name = self.validated_data.pop('method_name')
#         user = self.context['request'].user
#         print(user)
#         instance.venue = validated_data.get('venue', instance.venue)
#         # method_name = validated_data.get('method_name')
#         # instance.players = validated_data.get('players')
#         instance.status = validated_data.get('status', instance.status)
#         instance.to_user = validated_data.get('to_user', instance.to_user)
#         # print(method_name)
#         if method_name == 'accept':
#             instance.status = "A"
#             instance.updated_by = user
#             venue = Venue.objects.get(pk=instance.venue.pk)
#             venue.players.add(instance.to_user)
#             venue.save()
#         else:
#             instance.status = "R"
#             instance.updated_by = user
#             # venue.players.create(venue_id=venue, user_id=instance.to_user)
#         instance.save()
#         return instance
#
#
# # #######  END TEAM INVITES SERIALIZERS ######## #
#
# # #######  START LEAVE TEAM SERIALIZERS ######## #
#
#
# class LeaveVenueSerializer(serializers.ModelSerializer):
#     user_id = serializers.JSONField(required=False, default=None)
#
#     class Meta:
#         model = Venue
#         fields = ['id', 'name', 'user_id', 'longitude', 'latitude', 'appointment',  # 'invitation',
#                   'created_by', 'admin', 'country', 'city', 'players']
#
#     def update(self, instance, request, *args, **kwargs):
#         user_id = self.validated_data.pop('user_id')
#         user = self.context['request'].user
#
#         if user_id is None:
#             invitations = VenueInvite.objects.filter(to_user=user, venue=instance)
#             # print(str(invitations))
#             if invitations:
#                 for invitation in invitations:
#                     invitation.status = "L"
#                     invitation.active = False
#                     invitation.updated_by = user
#                     invitation.save()
#             instance.players.remove(user)
#             instance.updated_by = user
#         else:
#             invitations = VenueInvite.objects.filter(to_user=user_id, venue=instance)
#             # print('invitation = ' + str(invitations))
#             if invitations:
#                 for invitation in invitations:
#                     invitation.status = "K"
#                     # invitation.active = False
#                     invitation.updated_by = user
#                     invitation.save()
#             instance.players.remove(user_id)
#             instance.updated_by = user
#         instance.save()
#         return instance
#
#
# # ########## to add __all__ with extra fields ##########
#
# # def get_field_names(self, declared_fields, info):
# #     expanded_fields = super(LeaveVenueSerializer, self).get_field_names(declared_fields, info)
# #
# #     if getattr(self.Meta, 'extra_fields', None):
# #         return expanded_fields + self.Meta.extra_fields
# #     else:
# #         return expanded_fields
#
# # #######  END LEAVE TEAM SERIALIZERS ######## #
#
# # #######  START UN-BAN TEAM PLAYER SERIALIZERS ######## #
#
# class BannedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VenueInvite
#         fields = ('id', 'from_user', 'to_user', 'venue', 'status')
#
#     def update(self, instance, validated_data):
#         instance.venue = validated_data.get('venue', instance.venue)
#         instance.status = validated_data.get('status', instance.status)
#         instance.to_user = validated_data.get('to_user', instance.to_user)
#         instance.active = False
#         instance.save()
#         return instance
#
#
# # #######  END UN-BAN TEAM PLAYER SERIALIZERS ######## #
#
# # #######  START JOIN REQUEST SERIALIZERS ######## #
#
#
# class MyInvitationRequestsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VenueInvite
#         fields = ('id', 'from_user', 'to_user', 'date_time', 'venue', 'status')
#
#
# class MyInvitationRequestsCancelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VenueInvite
#         fields = ('id', 'from_user', 'to_user', 'date_time', 'venue', 'status')
#
#     def update(self, instance, validated_data):
#         instance.active = False
#         instance.status = "C"
#         instance.save()
#         return instance
#
### End Comment

