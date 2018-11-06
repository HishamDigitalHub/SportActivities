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

from VenueApp.models import (Venue, VenueImage, VenueVideo, VenueRating, VenuePreference)

from VenueApp.serializers import (
    VenueCreateSerializer,
    VenueImageCreateSerializer,
    VenueDetailsSerializer,
    VenueVideoCreateSerializer,
    MyVenueListSerializer,
    VenueRateSerializer,
    VenuePreferenceCreateSerializer)
from UserRegistrationApp.serializers import UserUpdateSerializer

from UserRegistrationApp.permissions import (
    IsOwnerOrReadOnly,
    AllowAnonymous,
    IsRelatedWithInvitation,
    IsMyInvitationRequest,
    IsPlayerInActivity,
    IsTeamAdminOrReadOnly, IsVenueAdminOrReadOnly)

from UserRegistrationApp.pagination import ProfileLimitPagination

# Create your views here.


class VenueDetailsAPIView(RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueDetailsSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination


class VenueDeleteAPIView(DestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]


class VenueImageAPICreateView(ListCreateAPIView):
    queryset = VenueImage.objects.all()
    serializer_class = VenueImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class VenueImageAPIUpdateView(RetrieveUpdateAPIView):
    queryset = VenueImage.objects.all()
    serializer_class = VenueImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class VenueVideoAPICreateView(ListCreateAPIView):
    queryset = VenueVideo.objects.all()
    serializer_class = VenueVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class VenueVideoAPIUpdateView(RetrieveUpdateAPIView):
    queryset = VenueVideo.objects.all()
    serializer_class = VenueVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class VenueAPIView(ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user, created_by=self.request.user, updated_by=self.request.user)

    def get_queryset(self):
        queryset_list = Venue.objects.all()
        query = self.request.GET.get("q", )
        if query:
            queryset_list = queryset_list.filter(
                Q(name__contains=query,)
            ).distinct()
        return queryset_list


class VenueUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MyVenueListAPIView(ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = MyVenueListSerializer
    permission_classes = [IsPlayerInActivity]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        return Venue.objects.filter(Venue.objects.filter(admin=self.request.user))


class VenueRateListAPIView(ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueRateSerializer
    permission_classes = [IsPlayerInActivity]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class VenuePreferenceCreateAPIView(CreateAPIView):
    serializer_class = VenuePreferenceCreateSerializer
    queryset = VenuePreference.objects.all()
    permission_classes = [IsAuthenticated, IsVenueAdminOrReadOnly]


class VenuePreferenceUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = VenuePreferenceCreateSerializer
    queryset = VenuePreference.objects.all()
    lookup_field = 'venue'
    permission_classes = [IsAuthenticated, IsVenueAdminOrReadOnly]

