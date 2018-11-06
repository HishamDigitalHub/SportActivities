from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.template.defaultfilters import length

from rest_framework.fields import CurrentUserDefault

from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueTogetherValidator

from UserRegistrationApp.models import Profile
from UserRegistrationApp.serializers import UserUpdateSerializer
from lookup.models import City, Country

from TeamApp.models import Team, TeamImage, TeamVideo, TeamPreference, TeamInvite  # , Sport, SportIcon

User = get_user_model()


# #######  START IMAGES SERIALIZERS ######## #

class TeamImageCreateSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = TeamImage
        fields = ('id', 'team', 'image',)
        # parser_classes = (MultiPartParser, FormParser,)

    def validate(self, data):
        # ..
        # ..

        # get the image data from request.FILES:
        self.context["image"] = self.context['request'].FILES.get("image")
        return data

    def create(self, validated_data):
        # set the thumbnail field:
        validated_data['image'] = self.context.get("image")
        user_profile = TeamImage.objects.create(**validated_data)
        return user_profile


class TeamImageSerializer(serializers.HyperlinkedModelSerializer):
    # team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    class Meta:
        model = TeamImage
        fields = ('image',)

    # def create(self, validated_data):
    #     team = Team.objects.get_or_create(validated_data)
    #     images_data = self.context.get('view').request.FILES
    #     for image_data in images_data.values():
    #         TeamImage.objects.create(team=team, image=image_data)
    #     return team


# #######  END IMAGES SERIALIZERS ######## #


# #######  START VIDEOS SERIALIZERS ######## #

class TeamVideoCreateSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        model = TeamVideo
        fields = ('team', 'video',)


class TeamVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeamVideo
        fields = ('video',)


# #######  END VIDEOS SERIALIZERS ######## #


# #######  START TEAMS SERIALIZERS ######## #

class TeamDetailsSerializer(ModelSerializer):
    images = TeamImageSerializer(source='teamimages', many=True)
    videos = TeamVideoSerializer(source='teamvideos', many=True)
    admin_name = SerializerMethodField()
    city_name = SerializerMethodField()
    country_name = SerializerMethodField()
    created_by_name = SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'admin',
            'admin_name',
            'id',
            'name',
            'longitude',
            'latitude',
            'score',
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


class MyTeamListSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'players']


class TeamCreateSerializer(ModelSerializer):
    # admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
    # many=False, default=serializers.CurrentUserDefault())
    # players = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    # city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    # score = serializers.IntegerField(read_only=True)
    # images = SerializerMethodField()
    # image = TeamImageSerializer(source='team', many=True)

    class Meta:
        model = Team
        fields = [
            # 'admin',
            'id',
            'name',
            'longitude',
            'latitude',
            'score',
            'country',
            'city',
            'players',
            'created_by',
            # 'image',
        ]

    def create(self, validated_data):
        obj = Team.objects.create(**validated_data)
        obj.players.add(obj.admin)
        # obj.active = True
        obj.save()
        return obj


# #######  END TEAMS SERIALIZERS ######## #

# #######  START TEAM INVITES SERIALIZERS ######## #


class TeamInviteCreateSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    method_name = serializers.SerializerMethodField()

    # serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    # to_user =

    def __init__(self, *args, **kwargs):
        from_user = kwargs['context']['request'].user
        # team = kwargs['context']['request'].team
        super(TeamInviteCreateSerializer, self).__init__(*args, **kwargs)
        self.fields['from_user'].queryset = User.objects.filter(id=from_user.id)
        # status = "A"
        # self.fields['status'].queryset = TeamInvite.objects.filter(status=status)

        # self.fields['from_user'].queryset = Team.objects.filter(players__in=from_user.id)

    class Meta:
        model = TeamInvite
        fields = ('id', 'from_user', 'to_user', 'date_time', 'team', 'method_name', 'status')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=TeamInvite.objects.filter(status="P", active=True),
                fields=('to_user', 'team'),
                message="You already sent an invitation request"
            ),
            serializers.UniqueTogetherValidator(
                queryset=TeamInvite.objects.filter(status="A", active=True),
                fields=('to_user', 'team'),
                message="this user already in the team"
            ),
            serializers.UniqueTogetherValidator(
                queryset=TeamInvite.objects.filter(status="K", active=True),
                fields=('to_user', 'team'),
                message="this user was kicked by admin of this team"
            ),
        ]

    def create(self, validated_data):
        obj = TeamInvite.objects.create(**validated_data)
        obj.status = "P"
        obj.active = True
        obj.save()
        return obj

    def get_method_name(self, *args, **kwargs):
        method_name = None  # kwargs['context']['request'].method_name
        return method_name


class MyTeamInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvite
        fields = ('id', 'from_user', 'date_time', 'team', 'status')


class TeamInviteAcceptDeclineSerializer(serializers.ModelSerializer):
    method_name = serializers.CharField(write_only=True, default="")

    class Meta:
        model = TeamInvite
        fields = ('id', 'from_user', 'to_user', 'team', 'method_name', 'status')

    def get_method_name(self, *args, **kwargs):
        method_name = None  # kwargs['context']['request'].method_name
        return method_name

    def update(self, instance, validated_data):
        method_name = self.validated_data.pop('method_name')

        instance.team = validated_data.get('team', instance.team)
        # method_name = validated_data.get('method_name')
        # instance.players = validated_data.get('players')
        instance.status = validated_data.get('status', instance.status)
        instance.to_user = validated_data.get('to_user', instance.to_user)
        # print(method_name)
        if method_name == 'accept':
            instance.status = "A"
            team = Team.objects.get(pk=instance.team.pk)
            team.players.add(instance.to_user)
            team.save()
        else:
            instance.status = "R"
            # team.players.create(team_id=team, user_id=instance.to_user)
        instance.save()
        return instance


# #######  END TEAM INVITES SERIALIZERS ######## #

# #######  START LEAVE TEAM SERIALIZERS ######## #


class LeaveTeamSerializer(serializers.ModelSerializer):
    user_id = serializers.JSONField(required=False, default=None)

    class Meta:
        model = Team
        fields = ['id', 'name', 'user_id', 'longitude', 'latitude', 'score',  # 'invitation',
                  'created_by', 'admin', 'country', 'city', 'players']

    def update(self, instance, request, *args, **kwargs):
        user_id = self.validated_data.pop('user_id')
        user = self.context['request'].user.pk

        if user_id is None:
            invitations = TeamInvite.objects.filter(to_user=user)
            # print(str(invitations))
            if invitations:
                for invitation in invitations:
                    invitation.status = "L"
                    invitation.active = False
                    invitation.save()
            instance.players.remove(user)
        else:
            invitations = TeamInvite.objects.filter(to_user=user_id)
            # print('invitation = ' + str(invitations))
            if invitations:
                for invitation in invitations:
                    invitation.status = "K"
                    # invitation.active = False
                    invitation.save()
            instance.players.remove(user_id)
        instance.save()
        return instance


# ########## to add __all__ with extra fields ##########

# def get_field_names(self, declared_fields, info):
#     expanded_fields = super(LeaveTeamSerializer, self).get_field_names(declared_fields, info)
#
#     if getattr(self.Meta, 'extra_fields', None):
#         return expanded_fields + self.Meta.extra_fields
#     else:
#         return expanded_fields

# #######  END LEAVE TEAM SERIALIZERS ######## #

# #######  START UN-BAN TEAM PLAYER SERIALIZERS ######## #

class BannedSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamInvite
        fields = ('id', 'from_user', 'to_user', 'team', 'status')

    def update(self, instance, validated_data):
        instance.team = validated_data.get('team', instance.team)
        instance.status = validated_data.get('status', instance.status)
        instance.to_user = validated_data.get('to_user', instance.to_user)
        instance.active = False
        instance.save()
        return instance

# #######  END UN-BAN TEAM PLAYER SERIALIZERS ######## #

# #######  START JOIN REQUEST SERIALIZERS ######## #


class MyInvitationRequestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvite
        fields = ('id', 'from_user', 'date_time', 'team', 'status')


class MyInvitationRequestsCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvite
        fields = ('id', 'from_user', 'date_time', 'team', 'status')

    def update(self, instance, validated_data):
        instance.active = False
        instance.status = "C"
        instance.save()
        return instance

# #######  END JOIN REQUEST PLAYER SERIALIZERS ######## #

# #######  START PREFERENCE SERIALIZERS ######## #


# ############################################
class TeamPreferenceCreateSerializer(ModelSerializer):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('B', 'Both'))
    # team = serializers.SerializerMethodField()
    team_name = SerializerMethodField()
    country_name = SerializerMethodField()
    city_name = SerializerMethodField()
    sport_name = SerializerMethodField()

    class Meta:

        model = TeamPreference
        fields = (
            'id',
            'team',
            'team_name',
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

    def get_team_name(self, obj):
        return str(obj.team.name)


# #######  END PREFERENCE SERIALIZERS ######## #

# def create(self, validated_data):
#     images_data = self.context.get('view').request.FILES
#     team = Team.objects.create(name=validated_data.get('name', 'no-title'),
#                                latitude=validated_data.get('latitude'),
#                                longitude=validated_data.get('longitude'),
#                                # score=validated_data.get('score'),
#                                country=validated_data.get('country'),
#                                city=validated_data.get('city'),
#                                # players=validated_data.get('players'),
#                                created=validated_data.get('created'),
#                                # images=validated_data.get('images'),
#                                )
#     for image_data in images_data.values():
#         TeamImage.objects.create(task=team, image=image_data)
#     return team

# def create(self, validated_data):

#     """
#     Overriding the default create method of the Model serializer.
#     :param validated_data: data containing all the details of student
#     :return: returns a successfully created student record
#     """
#     user_data = validated_data.pop('user')
#     user = UserUpdateSerializer.create(UserUpdateSerializer(), validated_data=user_data)
#
#     team, created = Team.objects.update_or_create(
#         user=user,
#         # user_id=validated_data.pop('user_id'),
#         country=validated_data.pop('country'),
#         city=validated_data.pop('city'),
#
#         longitude=validated_data.pop('longitude'),
#         latitude=validated_data.pop('latitude'),
#

# )
#
# return team

# class CitySerializer(ModelSerializer):

#     country = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
#
#     class Meta:
#
#         model = City
#         fields = ('name', 'country')
#
#     def get_country(self, obj):
#         return str(obj.country.name)

