from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

from rest_framework import routers

from PlayerApp.views import (
    PlayerImageAPICreateView,
    PlayerVideoAPICreateView,
)


urlpatterns = [
    # path('', include(router.urls)),
    url(r'^image-upload/$', PlayerImageAPICreateView.as_view(), name='upload-player-image'),
    url(r'^video-upload/$', PlayerVideoAPICreateView.as_view(), name='upload-player-video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
