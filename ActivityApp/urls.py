from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )

from rest_framework import routers

from ActivityApp.views import (
    ActivityAPIView,
    ActivityUpdateAPIView,
    ActivityImageAPICreateView,
    ActivityVideoAPICreateView,
    ActivityDetailsAPIView,
    ActivityInviteCreateAPIView,
    MyActivityListAPIView,
    MyActivityInvitationsAPIView,
    MyActivityInviteActionAPIView,
    LeaveActivityListAPIView,
    BanRemoveAPIView,
    BannedListAPIView,
    MyInvitationRequestListAPIView,
    MyInvitationRequestCancelAPIView,
    ActivityRateListAPIView,
    ActivityImageAPIUpdateView,
    ActivityVideoAPIUpdateView,
    ActivityDeleteAPIView, ActivityPreferenceCreateAPIView, ActivityPreferenceUpdateAPIView
)

# router = routers.DefaultRouter()
# router.APIRootView.register('list_city', CityAPIView)

# to access this patterns url(r'^api/activity/', include(('ActivityApp.urls', 'activities'), namespace='lookups')),

urlpatterns = [
                  # path('', include(router.urls)),
                  url(r'^image-upload/$', ActivityImageAPICreateView.as_view(), name='upload-image'),
                  url(r'^image-upload/(?P<pk>[\w-]+)/update/$', ActivityImageAPIUpdateView.as_view(), name='upload-image-update'),
                  url(r'^video-upload/(?P<pk>[\w-]+)/update/$', ActivityVideoAPIUpdateView.as_view(), name='upload-video-update'),
                  url(r'^video-upload/$', ActivityVideoAPICreateView.as_view(), name='upload-video'),
                  url(r'^join/invite/$', ActivityInviteCreateAPIView.as_view(), name='invite-join-activity'),
                  url(r'^my-invitations/$', MyActivityInvitationsAPIView.as_view(), name='list-join-activity-invitations'),
                  url(r'^my-invitation-request/$', MyInvitationRequestListAPIView.as_view(),
                      name='list-join-activity-requests'),
                  url(r'^my-invitation-request/(?P<pk>[\w-]+)/cancel/$', MyInvitationRequestCancelAPIView.as_view(),
                      name='cancel-invitation-request'),

                  url(r'^my/activities/$', MyActivityListAPIView.as_view(), name='my-activities'),

                  path('', ActivityAPIView.as_view(), name='activity_list'),
                  url(r'^(?P<pk>[\w-]+)/update/$', ActivityUpdateAPIView.as_view(), name='update_activity'),
                  url(r'^(?P<pk>[\w-]+)/leave/$', LeaveActivityListAPIView.as_view(), name='leave-activity'),
                  url(r'^(?P<pk>[\w-]+)/detail/$', ActivityDetailsAPIView.as_view(), name='activity_details'),
                  url(r'^invitation/(?P<pk>[\w-]+)/action/$', MyActivityInviteActionAPIView.as_view(),
                      name='action-activity-invitation'),
                  url(r'^banned/list/$', BannedListAPIView.as_view(), name='list_banned'),
                  url(r'^banned/(?P<pk>[\w-]+)/remove/$', BanRemoveAPIView.as_view(), name='remove_banned'),
                  url(r'^rate/$', ActivityRateListAPIView.as_view(), name='new_rate'),
                  url(r'^(?P<pk>[\w-]+)/delete/$', ActivityDeleteAPIView.as_view(), name='activity-delete'),
                  url(r'^preference/create/$', ActivityPreferenceCreateAPIView.as_view(), name='team-preference-create'),
                  url(r'^preference/(?P<activity>[\w-]+)/update/$', ActivityPreferenceUpdateAPIView.as_view(), name='team-delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
