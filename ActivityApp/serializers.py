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

from ActivityApp.models import ActivityRating, ActivityInvite, ActivityImage, Activity, ActivityVideo, \
    ActivityPreference

User = get_user_model()


# #######  START IMAGES SERIALIZERS ######## #

class ActivityImageCreateSerializer(serializers.HyperlinkedModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())

    class Meta:
        model = ActivityImage
        fields = ('activity', 'image',)


class ActivityImageSerializer(serializers.HyperlinkedModelSerializer):
    # activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    class Meta:
        model = ActivityImage
        fields = ('image',)

    # def create(self, validated_data):
    #     activity = Activity.objects.get_or_create(validated_data)
    #     images_data = self.context.get('view').request.FILES
    #     for image_data in images_data.values():
    #         ActivityImage.objects.create(activity=activity, image=image_data)
    #     return activity


# #######  END IMAGES SERIALIZERS ######## #


# #######  START VIDEOS SERIALIZERS ######## #

class ActivityVideoCreateSerializer(serializers.HyperlinkedModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())

    class Meta:
        model = ActivityVideo
        fields = ('activity', 'video',)


class ActivityVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityVideo
        fields = ('video',)


# #######  END VIDEOS SERIALIZERS ######## #


# #######  START TEAMS SERIALIZERS ######## #

class ActivityDetailsSerializer(ModelSerializer):
    images = ActivityImageSerializer(source='activityimages', many=True)
    videos = ActivityVideoSerializer(source='activityvideos', many=True)
    admin_name = SerializerMethodField()
    city_name = SerializerMethodField()
    country_name = SerializerMethodField()
    created_by_name = SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'admin',
            'admin_name',
            'id',
            'name',
            'longitude',
            'latitude',
            'appointment',
            'country',
            'country_name',
            'city',
            'city_name',
            'players',
            'created_by',
            'created_by_name',
            'images',
            'videos'
        ]

    def get_admin_name(self, obj):
        admin_obj = User.objects.get(pk=obj.admin.id)
        admin_name = str(admin_obj.first_name + ' ' + admin_obj.last_name)
        return admin_name

    def get_city_name(self, obj):
        city_obj = City.objects.get(pk=obj.city.id)
        city_name = city_obj.name
        return city_name

    def get_country_name(self, obj):
        country_obj = Country.objects.get(pk=obj.country.id)
        country_name = country_obj.name
        return country_name

    def get_created_by_name(self, obj):
        created_by_obj = User.objects.get(pk=obj.created_by.id)
        created_by_name = str(created_by_obj.first_name + ' ' + created_by_obj.last_name)
        return created_by_name


class MyActivityListSerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'players']


class ActivityCreateSerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            # 'admin',
            'id',
            'name',
            'longitude',
            'latitude',
            'appointment',
            'country',
            'city',
            'players',
            'created_by',
            'updated_date',
            # 'image',
        ]

    def create(self, validated_data):
        obj = Activity.objects.create(**validated_data)
        obj.players.add(obj.created_by)
        obj.save()
        return obj

# #######  END TEAMS SERIALIZERS ######## #

# #######  START TEAM INVITES SERIALIZERS ######## #


class ActivityInviteCreateSerializer(serializers.ModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    method_name = serializers.SerializerMethodField()

    # serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    # to_user =

    def __init__(self, *args, **kwargs):
        from_user = kwargs['context']['request'].user
        # activity = kwargs['context']['request'].activity
        super(ActivityInviteCreateSerializer, self).__init__(*args, **kwargs)
        self.fields['from_user'].queryset = User.objects.filter(id=from_user.id)
        # status = "A"
        # self.fields['status'].queryset = ActivityInvite.objects.filter(status=status)

        # self.fields['from_user'].queryset = Activity.objects.filter(players__in=from_user.id)

    class Meta:
        model = ActivityInvite
        fields = ('id', 'from_user', 'to_user', 'date_time', 'activity', 'method_name', 'status')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ActivityInvite.objects.filter(status="P", active=True),
                fields=('to_user', 'activity'),
                message="You already sent an invitation request"
            ),
            serializers.UniqueTogetherValidator(
                queryset=ActivityInvite.objects.filter(status="A", active=True),
                fields=('to_user', 'activity'),
                message="this user already in the activity"
            ),
            serializers.UniqueTogetherValidator(
                queryset=ActivityInvite.objects.filter(status="K", active=True),
                fields=('to_user', 'activity'),
                message="this user was kicked by admin of this activity"
            ),
        ]

    def create(self, validated_data):
        obj = ActivityInvite.objects.create(**validated_data)
        obj.status = "P"
        obj.active = True
        obj.save()
        return obj

    def get_method_name(self, *args, **kwargs):
        method_name = None  # kwargs['context']['request'].method_name
        return method_name


class MyActivityInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityInvite
        fields = ('id', 'from_user', 'date_time', 'activity', 'status')


class ActivityInviteAcceptDeclineSerializer(serializers.ModelSerializer):
    method_name = serializers.CharField(write_only=True, default="")

    class Meta:
        model = ActivityInvite
        fields = ('id', 'from_user', 'to_user', 'activity', 'method_name', 'status')

    def get_method_name(self, *args, **kwargs):
        method_name = None  # kwargs['context']['request'].method_name
        return method_name

    def update(self, instance, validated_data):
        method_name = self.validated_data.pop('method_name')
        user = self.context['request'].user
        print(user)
        instance.activity = validated_data.get('activity', instance.activity)
        # method_name = validated_data.get('method_name')
        # instance.players = validated_data.get('players')
        instance.status = validated_data.get('status', instance.status)
        instance.to_user = validated_data.get('to_user', instance.to_user)
        # print(method_name)
        if method_name == 'accept':
            instance.status = "A"
            instance.updated_by = user
            activity = Activity.objects.get(pk=instance.activity.pk)
            activity.players.add(instance.to_user)
            activity.save()
        else:
            instance.status = "R"
            instance.updated_by = user
            # activity.players.create(activity_id=activity, user_id=instance.to_user)
        instance.save()
        return instance


# #######  END TEAM INVITES SERIALIZERS ######## #

# #######  START LEAVE TEAM SERIALIZERS ######## #


class LeaveActivitySerializer(serializers.ModelSerializer):
    user_id = serializers.JSONField(required=False, default=None)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'user_id', 'longitude', 'latitude', 'appointment',  # 'invitation',
                  'created_by', 'admin', 'country', 'city', 'players']

    def update(self, instance, request, *args, **kwargs):
        user_id = self.validated_data.pop('user_id')
        user = self.context['request'].user

        if user_id is None:
            invitations = ActivityInvite.objects.filter(to_user=user, activity=instance)
            # print(str(invitations))
            if invitations:
                for invitation in invitations:
                    invitation.status = "L"
                    invitation.active = False
                    invitation.updated_by = user
                    invitation.save()
            instance.players.remove(user)
            instance.updated_by = user
        else:
            invitations = ActivityInvite.objects.filter(to_user=user_id, activity=instance)
            # print('invitation = ' + str(invitations))
            if invitations:
                for invitation in invitations:
                    invitation.status = "K"
                    # invitation.active = False
                    invitation.updated_by = user
                    invitation.save()
            instance.players.remove(user_id)
            instance.updated_by = user
        instance.save()
        return instance


# ########## to add __all__ with extra fields ##########

# def get_field_names(self, declared_fields, info):
#     expanded_fields = super(LeaveActivitySerializer, self).get_field_names(declared_fields, info)
#
#     if getattr(self.Meta, 'extra_fields', None):
#         return expanded_fields + self.Meta.extra_fields
#     else:
#         return expanded_fields

# #######  END LEAVE TEAM SERIALIZERS ######## #

# #######  START UN-BAN TEAM PLAYER SERIALIZERS ######## #

class BannedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityInvite
        fields = ('id', 'from_user', 'to_user', 'activity', 'status')

    def update(self, instance, validated_data):
        instance.activity = validated_data.get('activity', instance.activity)
        instance.status = validated_data.get('status', instance.status)
        instance.to_user = validated_data.get('to_user', instance.to_user)
        instance.active = False
        instance.save()
        return instance


# #######  END UN-BAN TEAM PLAYER SERIALIZERS ######## #

# #######  START JOIN REQUEST SERIALIZERS ######## #


class MyInvitationRequestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityInvite
        fields = ('id', 'from_user', 'to_user', 'date_time', 'activity', 'status')


class MyInvitationRequestsCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityInvite
        fields = ('id', 'from_user', 'to_user', 'date_time', 'activity', 'status')

    def update(self, instance, validated_data):
        instance.active = False
        instance.status = "C"
        instance.save()
        return instance


class ActivityRateSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     created_by = kwargs['context']['request'].user
    #     super(ActivityRateSerializer, self).__init__(*args, **kwargs)
    #     self.fields['created_by'].queryset = User.objects.filter(id=created_by.id)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                    default=serializers.CurrentUserDefault())
    # activity = serializers.IntegerField()

    # activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())

    def validate(self, attrs):
        attrs = super(ActivityRateSerializer, self).validate(attrs)  # calling default validation
        activity = attrs['activity']
        rate = attrs['rate']
        print(activity.id)
        print(attrs['activity'])
        already_rated = ActivityRating.objects.filter(created_by=self.context['request'].user, activity=activity.id)
        if not Activity.objects.filter(id=activity.id, players=self.context['request'].user).exists():
            raise serializers.ValidationError("To rate, you should be a member in this activity")
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
        model = ActivityRating
        fields = ['id', 'activity', 'rate', 'created_by']


# ############################################
class ActivityPreferenceCreateSerializer(ModelSerializer):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))
    # team = serializers.SerializerMethodField()
    activity_name = SerializerMethodField()
    country_name = SerializerMethodField()
    city_name = SerializerMethodField()
    sport_name = SerializerMethodField()

    class Meta:

        model = ActivityPreference
        fields = (
            'id',
            'activity',
            'activity_name',
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

    def get_activity_name(self, obj):
        return str(obj.activity.name)

# #######  END PREFERENCE SERIALIZERS ######## #




        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=ActivityRating.objects.all(),
        #         fields=('created_by', 'activity'),
        #         message="You already rated this activity"
        #     )]

    # def create(self, validated_data):
    #
    #     obj = ActivityRating.objects.create(**validated_data)
    #     obj.save()
    #     return obj

    # def can_rate(self):
    #     created_by = self.instance.created_by
    #     if created_by in ActivityRating.activity.players:
    #         raise serializers.ValidationError('This field must be an even number.')
    #     else:
    #         raise serializers.ValidationError('can rate')
