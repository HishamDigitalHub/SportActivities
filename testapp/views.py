from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from .models import Json1Test
from .serializers import Json1TestSerializer, TestJsonCreateSerializer


class TestJson(viewsets.ModelViewSet):
    queryset = Json1Test.objects.all()
    serializer_class = Json1TestSerializer


class TestJsonCreateAPIView(CreateAPIView):
    queryset = Json1Test.objects.all()
    serializer_class = TestJsonCreateSerializer