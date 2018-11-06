from django.db.models import Q

from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django_filters.conf import settings
from djoser.compat import get_user_email
from djoser.views import UserView

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    DjangoModelPermissions,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
# ###################################################
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# #################################################
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.serializers import ModelSerializer

from UserRegistrationApp.models import Profile, UserPreference
from UserRegistrationApp.serializers import (ProfileCreateSerializer,
                                             ProfileListSerializer,
                                             ProfileDetailSerializer,
                                             ProfileUpdateSerializer,
                                             UserCreateSerializer,
                                             UserUpdateSerializer,
                                             UserSerializer,
                                             PreferenceCreateSerializer,
                                             )

from .permissions import IsOwnerOrReadOnly, AllowAnonymous, IsProfileOwnerOrReadOnly

from .pagination import ProfileLimitPagination

# ######### START USER VIEWS ##########

User = get_user_model()


class UserCreateAPIView(CreateAPIView):

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAnonymous]

# class UserUpdateAPIView(UpdateAPIView):
#     serializer_class = UserUpdateSerializer
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
# ######### END USER VIEWS ###########

# ######### START PROFILE VIEWS ##########
# Just for view


class ProfileCreateAPIView(ListCreateAPIView):

    """
    A class based view for creating and fetching student records
    """
    permission_classes = (AllowAnonymous, AllowAny)
    pagination_class = ProfileLimitPagination
    serializer_class = ProfileCreateSerializer
    queryset = Profile.objects.all()

    def get(self, format: object = None) -> object:
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        profiles = Profile.objects.all()
        serializer = ProfileCreateSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        serializer = ProfileCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            # serializer.create(validated_data=request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class ProfileALLListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    pagination_class = ProfileLimitPagination  # PageNumberPagination


class ProfileListAPIView(ListAPIView):
    # queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__first_name', 'mobile_no', 'user__last_name']
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        # queryset_list = super(ProfileListAPIView, self).get_queryset(*args, **kwargs)
        # if you want to use the above line you should add the first comment in the class
        # but we can use different way by add queryset = Profile.objects.all() in the function

        queryset_list = Profile.objects.filter(public_profile_ind=True)
        query = self.request.GET.get("q", )
        # should add self. before request.GET..etc. because it is ClassBasedView

        if query:
            queryset_list = queryset_list.filter(
                Q(user__first_name__contains=query) |
                Q(user__last_name__contains=query) |
                Q(user__email__contains=query) |
                Q(user__username__contains=query) |
                Q(mobile_no__icontains=query) |
                Q(facebook_id__icontains=query) |
                Q(google_id__icontains=query) |
                Q(longitude__icontains=query) |
                Q(latitude__icontains=query) |
                Q(height__icontains=query) |
                Q(weight__icontains=query)
            ).distinct()
        return queryset_list

    # permission_classes = (IsAuthenticated, IsAdminUser,)
    # pagination_class =


class ProfileDetailAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'user' # if i want to find without using pk


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    # lookup_field = 'user'
    # lookup_url_kwarg = 'abc'
    #
    # def perform_update(self, serializer):
    #     # super(ProfileUpdateAPIView, self).perform_update(serializer)
    #
    #     serializer.save(user=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)


class ProfileDeleteAPIView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # lookup_field = 'user'

# Create your views here.
#
# from rest_framework import viewsets, generics, mixins, permissions
# from rest_framework.parsers import FormParser, MultiPartParser
#
# from .models import Profile
# from .serializers import ProfileSerializer
#
#
# class ProfileView(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     print('dasdasdasdadasdasdsd')


# User = get_user_model()


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request):
        self.object = self.get_object()
        serializer = UserSerializer(self.object, data=request.data)
        if serializer.is_valid():
            self.object.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PreferenceCreateAPIView(CreateAPIView):
    serializer_class = PreferenceCreateSerializer
    queryset = UserPreference.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PreferenceUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PreferenceCreateSerializer
    queryset = UserPreference.objects.all()
    lookup_field = 'user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
