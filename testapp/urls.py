from django.conf.urls import include, url
from django.urls import path
from . import views
from testapp.views import TestJson, TestJsonCreateAPIView

from rest_framework import routers


router = routers.DefaultRouter()
router.register('Json2', TestJson)
router.register('json', TestJson)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^create1/$', TestJsonCreateAPIView.as_view(), name='create_test')
]
