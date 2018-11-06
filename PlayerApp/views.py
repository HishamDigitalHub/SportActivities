from django.shortcuts import render


from django.db.models import Q


from rest_framework.permissions import (
    AllowAny,)


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

from PlayerApp.models import (PlayerImage, PlayerVideo)


from PlayerApp.serializers import (
    PlayerImageCreateSerializer,
    PlayerImageSerializer,
    PlayerVideoCreateSerializer,
    PlayerVideoSerializer,
                             )
from UserRegistrationApp.serializers import UserUpdateSerializer

from UserRegistrationApp.permissions import IsOwnerOrReadOnly, AllowAnonymous

from UserRegistrationApp.pagination import ProfileLimitPagination

# Create your views here.


class PlayerImageAPICreateView(ListCreateAPIView):
    queryset = PlayerImage.objects.all()
    serializer_class = PlayerImageCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlayerVideoAPICreateView(ListCreateAPIView):
    queryset = PlayerVideo.objects.all()
    serializer_class = PlayerVideoCreateSerializer
    permission_classes = [AllowAny, AllowAnonymous]
    pagination_class = ProfileLimitPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
