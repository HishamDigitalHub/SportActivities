from django.shortcuts import render
from django_filters import rest_framework as filters

from django.db.models import Q

from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated)

from rest_framework import serializers

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

from ActivityApp.models import (Activity, ActivityImage, ActivityVideo, ActivityInvite, ActivityRating,
                                ActivityPreference)

from ActivityApp.serializers import (
    ActivityCreateSerializer,
    ActivityImageCreateSerializer,
    ActivityDetailsSerializer,
    ActivityVideoCreateSerializer,
    ActivityInviteCreateSerializer,
    MyActivityListSerializer,
    ActivityInviteAcceptDeclineSerializer,
    MyActivityInviteSerializer,
    LeaveActivitySerializer,
    BannedSerializer,
    MyInvitationRequestsListSerializer,
    MyInvitationRequestsCancelSerializer,
    ActivityRateSerializer,
    ActivityPreferenceCreateSerializer)
from UserRegistrationApp.serializers import UserUpdateSerializer

from UserRegistrationApp.permissions import (
    IsOwnerOrReadOnly,
    AllowAnonymous,
    IsRelatedWithInvitation,
    IsMyInvitationRequest,
    IsPlayerInActivity,
    IsTeamAdminOrReadOnly)

from UserRegistrationApp.pagination import ProfileLimitPagination

# Create your views here.


class ActivityDetailsAPIView(RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivityDetailsSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination


class ActivityDeleteAPIView(DestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivityDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ActivityImageAPICreateView(ListCreateAPIView):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class ActivityImageAPIUpdateView(RetrieveUpdateAPIView):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ActivityVideoAPICreateView(ListCreateAPIView):
    queryset = ActivityVideo.objects.all()
    serializer_class = ActivityVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class ActivityVideoAPIUpdateView(RetrieveUpdateAPIView):
    queryset = ActivityVideo.objects.all()
    serializer_class = ActivityVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ActivityAPIView(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivityCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user, created_by=self.request.user, updated_by=self.request.user)

    def get_queryset(self):
        queryset_list = Activity.objects.all()
        query = self.request.GET.get("q", )
        if query:
            queryset_list = queryset_list.filter(
                Q(name__contains=query,)
            ).distinct()
        return queryset_list


class ActivityUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivityCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ActivityInviteCreateAPIView(ListCreateAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = ActivityInviteCreateSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user, created_by=self.request.user, updated_by=self.request.user)

        # team = TeamInvite.objects.filter(from_user__players=self.request.user)


class MyActivityInvitationsAPIView(ListAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = MyActivityInviteSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return ActivityInvite.objects.filter(to_user=self.request.user, status="P")


class BanRemoveAPIView(RetrieveUpdateAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = BannedSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        activity = ActivityInvite.objects.filter(activity__admin=self.request.user)
        # print(team)
        return activity

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class BannedListAPIView(ListAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = BannedSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        activity = ActivityInvite.objects.filter(activity__admin=self.request.user)
        # print(team)
        return activity


class MyActivityInviteActionAPIView(RetrieveUpdateAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = ActivityInviteAcceptDeclineSerializer
    permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return ActivityInvite.objects.filter(to_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MyActivityListAPIView(ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = MyActivityListSerializer
    permission_classes = [IsPlayerInActivity]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return Activity.objects.filter(players=self.request.user) or Activity.objects.filter(admin=self.request.user)


class MyInvitationRequestListAPIView(ListAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = MyInvitationRequestsListSerializer
    permission_classes = [IsMyInvitationRequest]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return ActivityInvite.objects.filter(from_user=self.request.user, status="P", active=True)


class MyInvitationRequestCancelAPIView(RetrieveUpdateAPIView):
    queryset = ActivityInvite.objects.all()
    serializer_class = MyInvitationRequestsCancelSerializer
    permission_classes = [IsMyInvitationRequest]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return ActivityInvite.objects.filter(from_user=self.request.user, status="P", active=True)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class LeaveActivityListAPIView(RetrieveUpdateAPIView):
    queryset = Activity.objects.all()
    serializer_class = LeaveActivitySerializer
    # permission_classes = [IsRelatedWithInvitation]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        return Activity.objects.filter(players=self.request.user) or Activity.objects.filter(admin=self.request.user)

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


class ActivityRateListAPIView(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivityRateSerializer
    permission_classes = [IsPlayerInActivity]
    pagination_class = ProfileLimitPagination

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return ActivityRating.objects.all()
    #     else:
    #         return ActivityRating.objects.filter(activity__players=self.request.user)
    #  (activity__players=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ActivityPreferenceCreateAPIView(CreateAPIView):
    serializer_class = ActivityPreferenceCreateSerializer
    queryset = ActivityPreference.objects.all()
    permission_classes = [IsAuthenticated, IsTeamAdminOrReadOnly]


class ActivityPreferenceUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ActivityPreferenceCreateSerializer
    queryset = ActivityPreference.objects.all()
    lookup_field = 'activity'
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
