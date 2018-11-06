from django.conf.urls import include, url
from django.urls import path

from UserRegistrationApp.views import (
    ProfileCreateAPIView,
    ProfileALLListAPIView,
    ProfileDetailAPIView,
    ProfileDeleteAPIView,
    ProfileUpdateAPIView,
    ProfileListAPIView,
    UserUpdateAPIView,
    PreferenceCreateAPIView,
    PreferenceUpdateAPIView,
)

from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('Registration1', ProfileListAPIView)

# to access this patterns url(r'^api/profile/', include('UserRegistrationApp.urls')),

urlpatterns = [
    path('query/', ProfileListAPIView.as_view(), name='query_list'),
    path('create/', ProfileCreateAPIView.as_view(), name='create'),
    path('create-preference/', PreferenceCreateAPIView.as_view(), name='create_preference'),
    # url(r'^(?P<pk>\d+)/$', ProfileDetailAPIRetrieve.as_view(), name='detail'),
    url(r'^(?P<user>[\w-]+)/$', ProfileDetailAPIView.as_view(), name='details'),
    url(r'^(?P<pk>[\w-]+)/delete/$', ProfileDeleteAPIView.as_view(), name='delete'),
    url(r'^(?P<pk>[\w-]+)/update/$', ProfileUpdateAPIView.as_view(), name='update_profile'),
    url(r'^(?P<pk>[\w-]+)/update-user/$', UserUpdateAPIView.as_view(), name='update_user'),
    url(r'^(?P<user>[\w-]+)/update-preference/$', PreferenceUpdateAPIView.as_view(), name='update_preference'),
    path('', ProfileALLListAPIView.as_view(), name='list'),

    # url(r'^profile/$', ProfileRecordView.as_view(), name='students_list'),

    # cant use create here because it created with user table

    # url(r'^change/(?P<username>[\w-]+)/$',
    # ProfileView.as_view(actions={'get': 'retrieve', 'post': 'update'}), name='changeProfile'),

]
