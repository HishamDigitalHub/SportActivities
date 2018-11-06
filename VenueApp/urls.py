from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )

from rest_framework import routers

from VenueApp.views import (
    VenueAPIView,
    VenueUpdateAPIView,
    VenueImageAPICreateView,
    VenueVideoAPICreateView,
    VenueDetailsAPIView,
    MyVenueListAPIView,
    VenueRateListAPIView,
    VenueImageAPIUpdateView,
    VenueVideoAPIUpdateView,
    VenueDeleteAPIView,
    VenuePreferenceCreateAPIView,
    VenuePreferenceUpdateAPIView,)

# router = routers.DefaultRouter()
# router.APIRootView.register('list_city', CityAPIView)

# to access this patterns url(r'^api/venue/', include(('VenueApp.urls', 'venues'), namespace='venue')),

urlpatterns = [
                  # path('', include(router.urls)),
                  url(r'^image-upload/$', VenueImageAPICreateView.as_view(), name='upload-image'),
                  url(r'^image-upload/(?P<pk>[\w-]+)/update/$', VenueImageAPIUpdateView.as_view(), name='upload-image-update'),
                  url(r'^video-upload/(?P<pk>[\w-]+)/update/$', VenueVideoAPIUpdateView.as_view(), name='upload-video-update'),
                  url(r'^video-upload/$', VenueVideoAPICreateView.as_view(), name='upload-video'),
                  url(r'^my/venues/$', MyVenueListAPIView.as_view(), name='my-venues'),

                  path('', VenueAPIView.as_view(), name='Venue_list'),
                  url(r'^(?P<pk>[\w-]+)/update/$', VenueUpdateAPIView.as_view(), name='update_venue'),
                  url(r'^(?P<pk>[\w-]+)/detail/$', VenueDetailsAPIView.as_view(), name='venue_details'),
                  url(r'^rate/$', VenueRateListAPIView.as_view(), name='new_rate'),
                  url(r'^(?P<pk>[\w-]+)/delete/$', VenueDeleteAPIView.as_view(), name='venue-delete'),
                  url(r'^preference/create/$', VenuePreferenceCreateAPIView.as_view(),
                      name='team-preference-create'),
                  url(r'^preference/(?P<venue>[\w-]+)/update/$', VenuePreferenceUpdateAPIView.as_view(),
                      name='team-delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
