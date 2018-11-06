from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    DjangoModelPermissions,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,

)

from lookup.models import (Country, City, Sport, SportIcon)


from lookup.serializers import (
                             CountrySerializer,
                             CitySerializer,
                             CityOnlySerializer,
                             SportListSerializer,
                             SportDetailSerializer
                             )

from UserRegistrationApp.permissions import IsOwnerOrReadOnly, AllowAnonymous

from UserRegistrationApp.pagination import ProfileLimitPagination

# Create your views here.


class CountryAPIView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination


class CityAPIView(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination


class CityBasedCountry(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityOnlySerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        # queryset_list = super(ProfileListAPIView, self).get_queryset(*args, **kwargs)
        # if you want to use the above line you should add the first comment in the class
        # but we can use different way by add queryset = Profile.objects.all() in the function

        queryset_list = City.objects.all()
        query = self.request.GET.get("q", )
        # should add self. before request.GET..etc. because it is ClassBasedView

        if query:
            queryset_list = queryset_list.filter(
                Q(country__in=query)
            ).distinct()
        return queryset_list

    # If i used CreateAPIView should use the following code
    #
    # def post(self, request):
    #
    #     serializer = CitySerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=ValueError):
    #         # serializer.create(validated_data=request.data)
    #         serializer.save() # to set foreign key from existing value
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error_messages,
    #                     status=status.HTTP_400_BAD_REQUEST)


class SportAPIView(ListCreateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportListSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def get_queryset(self):
        queryset_list = Sport.objects.all()
        query = self.request.GET.get("q", )
        if query:
            queryset_list = queryset_list.filter(
                Q(name__in=query, ),
                Q(description__contains=query, ),

            ).distinct()
            # if not queryset_list:
            #     raise APIException("there is no team like this name")
        return queryset_list


class SportDetailAPIView(RetrieveAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportDetailSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    #
    # def get_queryset(self):
    #     queryset_list = Sport.objects.all()
    #     query = self.request.GET.get("q", )
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(name__in=query, ),
    #             Q(description__contains=query, ),
    #
    #         ).distinct()
    #         # if not queryset_list:
    #         #     raise APIException("there is no team like this name")
    #     return queryset_list


class SportUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProfileLimitPagination

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class SportDeleteAPIView(DestroyAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportListSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    # pagination_class = ProfileLimitPagination