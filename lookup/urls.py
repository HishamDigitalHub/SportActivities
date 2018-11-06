from django.urls import path
from django.conf import settings
from django.conf.urls import url, include

from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

from rest_framework import routers

from lookup.views import (
    CityAPIView,
    CountryAPIView,
    CityBasedCountry,
    SportAPIView,
    SportUpdateAPIView,
    SportDeleteAPIView,
    SportDetailAPIView)



# router = routers.DefaultRouter()
# router.APIRootView.register('list_city', CityAPIView)

# to access this patterns url(r'^api/lookups/', include(('lookup.urls', 'lookups'), namespace='lookups')),

urlpatterns = [
    # path('', include(router.urls)),
    path('city/query/', CityBasedCountry.as_view(), name='query_list'),
    path('city/', CityAPIView.as_view(), name='list_city'),
    path('country/', CountryAPIView.as_view(), name='list_country'),
    # url(r'^(?P<pk>[\w-]+)/$', CountryAPIView.as_view(), name='details_country'),
    # url(r'^(?P<pk>[\w-]+)/delete/$', CountryAPIView.as_view(), name='delete_country'),
    # url(r'^(?P<pk>[\w-]+)/update/country/$', CountryAPIView.as_view(), name='update_country'),
    # url(r'^(?P<pk>[\w-]+)/$', CityAPIView.as_view(), name='details-city'),
    # url(r'^(?P<pk>[\w-]+)/delete/$', CityAPIView.as_view(), name='delete-city'),
    # url(r'^(?P<pk>[\w-]+)/update-city/$', CityAPIView.as_view(), name='update_country'),
    url(r'^query-city-of-country/$', CityBasedCountry.as_view(), name='list_city_of_country'),
    url(r'^sport/$', SportAPIView.as_view(), name='sport_list'),
    url(r'^sport/(?P<pk>[\w-]+)/update/$', SportUpdateAPIView.as_view(), name='update_sport'),
    url(r'^sport/(?P<pk>[\w-]+)/detail/$', SportDetailAPIView.as_view(), name='sport_details'),
    url(r'^sport/(?P<pk>[\w-]+)/delete/$', SportDeleteAPIView.as_view(), name='sport-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
