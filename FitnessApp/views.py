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

from FitnessApp.models import (Workout, Fitness, Exercise, ExerciseIcon,
                               ExerciseImage, ExerciseRating, ExerciseVideo)

from FitnessApp.serializers import (ExerciseImageCreateSerializer,
                                    ExerciseVideoCreateSerializer,
                                    ExerciseImageSerializer,
                                    ExerciseVideoSerializer,
                                    ExerciseIconCreateSerializer,
                                    ExerciseIconSerializer)

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


class ExerciseImageAPICreateView(ListCreateAPIView):
    queryset = ExerciseImage.objects.all()
    serializer_class = ExerciseImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class ExerciseImageAPIUpdateView(RetrieveUpdateAPIView):
    queryset = ExerciseImage.objects.all()
    serializer_class = ExerciseImageSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ExerciseVideoAPICreateView(ListCreateAPIView):
    queryset = ExerciseVideo.objects.all()
    serializer_class = ExerciseVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class ExerciseVideoAPIUpdateView(RetrieveUpdateAPIView):
    queryset = ExerciseVideo.objects.all()
    serializer_class = ExerciseVideoSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ExerciseIconAPICreateView(ListCreateAPIView):
    queryset = ExerciseIcon.objects.all()
    serializer_class = ExerciseIconCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination



    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class ExerciseIconAPIUpdateView(RetrieveUpdateAPIView):
    queryset = ExerciseIcon.objects.all()
    serializer_class = ExerciseIconSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
