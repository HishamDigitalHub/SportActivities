from django.shortcuts import render
from django_filters import rest_framework as filters


from django.db.models import Q
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.exceptions import APIException

from rest_framework.permissions import (
    AllowAny, IsAuthenticated)

from rest_framework import serializers, parsers

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,

)
from rest_framework.response import Response
from rest_framework import filters

from ActivityApp.models import Activity
from TeamApp.models import (Team, TeamImage, TeamVideo, TeamInvite, TeamPreference) #, Sport, SportIcon)


from TeamApp.serializers import (
    TeamCreateSerializer,
    TeamImageCreateSerializer,
    TeamDetailsSerializer,
    TeamVideoCreateSerializer,
    TeamInviteCreateSerializer,
    MyTeamListSerializer,
    TeamInviteAcceptDeclineSerializer,
    MyTeamInviteSerializer,
    LeaveTeamSerializer,
    BannedSerializer,
    MyInvitationRequestsListSerializer,
    MyInvitationRequestsCancelSerializer,
    TeamPreferenceCreateSerializer,
)
from UserRegistrationApp.models import Profile
from UserRegistrationApp.serializers import UserUpdateSerializer, ProfileListSerializer

from UserRegistrationApp.permissions import (
    IsOwnerOrReadOnly,
    AllowAnonymous,
    IsRelatedWithInvitation,
    IsMyInvitationRequest,
    IsTeamAdminOrReadOnly)

from UserRegistrationApp.pagination import ProfileLimitPagination

# Create your views here.


class TeamDetailsAPIView(RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailsSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination


class TeamDeleteAPIView(DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TeamImageAPICreateView(ListCreateAPIView):
    queryset = TeamImage.objects.all()
    serializer_class = TeamImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    # def perform_create(self, serializer):
    #     import requests
    #     files = {'thumb': open('D:/thumb.jpg', 'rb'), 'preview': open('D:/preview.jpg', 'rb')}
    #     r = requests.put('/api/team/image-upload/', data={'key': 'value', 'key2': 'value2'}, files=files)
    #     print(r.status_code)
    #     serializer.save(created_by=self.request.user, updated_by=self.request.user)


class TeamVideoAPICreateView(ListCreateAPIView):
    queryset = TeamVideo.objects.all()
    serializer_class = TeamVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class TeamAPIView(ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user, created_by=self.request.user, updated_by=self.request.user)

    def get_queryset(self):
        queryset_list = Team.objects.all()
        query = self.request.GET.get("q", )
        if query:
            queryset_list = queryset_list.filter(
                Q(name__contains=query,)
            ).distinct()
            # if not queryset_list:
            #     raise APIException("there is no team like this name")
        return queryset_list


class TeamUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class TeamInviteCreateAPIView(ListCreateAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = TeamInviteCreateSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

        # team = TeamInvite.objects.filter(from_user__players=self.request.user)


class MyTeamInvitationsAPIView(ListAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = MyTeamInviteSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return TeamInvite.objects.filter(to_user=self.request.user, status="P")


class BanRemoveAPIView(RetrieveUpdateAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = BannedSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):

        team = TeamInvite.objects.filter(team__admin=self.request.user)
        # print(team)
        return team

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class BannedListAPIView(ListAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = BannedSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):

        team = TeamInvite.objects.filter(team__admin=self.request.user)
        # print(team)
        return team


class MyTeamInviteActionAPIView(RetrieveUpdateAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = TeamInviteAcceptDeclineSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return TeamInvite.objects.filter(to_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MyTeamListAPIView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = MyTeamListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return Team.objects.filter(players=self.request.user) and Team.objects.filter(admin=self.request.user)


class MyInvitationRequestListAPIView(ListAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = MyInvitationRequestsListSerializer
    permission_classes = [IsMyInvitationRequest]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return TeamInvite.objects.filter(from_user=self.request.user, status="P", active=True)


class MyInvitationRequestCancelAPIView(RetrieveUpdateAPIView):
    queryset = TeamInvite.objects.all()
    serializer_class = MyInvitationRequestsCancelSerializer
    permission_classes = [IsMyInvitationRequest]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return TeamInvite.objects.filter(from_user=self.request.user, status="P", active=True)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class LeaveTeamListAPIView(RetrieveUpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = LeaveTeamSerializer
    # permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return Team.objects.filter(players=self.request.user) or Team.objects.filter(admin=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        # Note: Additionally 'response' will also be added to the context,
        #       by the Response object.
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }


class TeamPreferenceCreateAPIView(CreateAPIView):
    serializer_class = TeamPreferenceCreateSerializer
    queryset = TeamPreference.objects.all()
    permission_classes = [IsAuthenticated, IsTeamAdminOrReadOnly]


class TeamPreferenceUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = TeamPreferenceCreateSerializer
    queryset = TeamPreference.objects.all()
    lookup_field = 'team'
    permission_classes = [IsAuthenticated, IsTeamAdminOrReadOnly]

    # def get_serializer_context(self):
    #     return {'request': self.request}

    # def get_queryset(self):
    #     user = self.request.user
    #     team = Team.objects.filter(players__admin=user)
    #     return team
    #
    # def validate(self, data):
    #     if not data.get('page', None):
    #         return data
    #     location = self.context.get('location')
    #     if location == data['page']:
    #         return data
    #     raise serializers.ValidationError('Error.')
