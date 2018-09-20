from django.conf.urls import include
from django.urls import path

from UserRegistrationApp.views import UserRegistrationView

from rest_framework import routers


router = routers.DefaultRouter()
router.register('Registration', UserRegistrationView)


urlpatterns = [
    path('regi/', include(router.urls)),

]
