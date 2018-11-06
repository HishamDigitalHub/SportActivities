from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.filters import SearchFilter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )

from rest_framework import routers

from TeamApp.views import (
    TeamAPIView,
    TeamUpdateAPIView,
    TeamImageAPICreateView,
    TeamVideoAPICreateView,
    TeamDetailsAPIView,
    TeamInviteCreateAPIView,
    MyTeamListAPIView,
    MyTeamInvitationsAPIView,
    MyTeamInviteActionAPIView,
    LeaveTeamListAPIView,
    BanRemoveAPIView,
    BannedListAPIView,
    MyInvitationRequestListAPIView,
    MyInvitationRequestCancelAPIView,
    TeamDeleteAPIView,
    TeamPreferenceCreateAPIView, TeamPreferenceUpdateAPIView)

# router = routers.DefaultRouter()
# router.APIRootView.register('list_city', CityAPIView)

# to access this patterns url(r'^api/team/', include(('TeamApp.urls', 'teams'), namespace='lookups')),

urlpatterns = [
                  # path('', include(router.urls)),
                  url(r'^image-upload/$', TeamImageAPICreateView.as_view(), name='upload-image'),
                  url(r'^video-upload/$', TeamVideoAPICreateView.as_view(), name='upload-video'),
                  url(r'^join/invite/$', TeamInviteCreateAPIView.as_view(), name='invite-join-team'),
                  url(r'^my-invitations/$', MyTeamInvitationsAPIView.as_view(), name='list-join-team-invitations'),
                  url(r'^my-invitation-request/$', MyInvitationRequestListAPIView.as_view(),
                      name='list-join-team-requests'),
                  url(r'^my-invitation-request/(?P<pk>[\w-]+)/cancel/$', MyInvitationRequestCancelAPIView.as_view(),
                      name='cancel-invitation-request'),

                  url(r'^my/teams/$', MyTeamListAPIView.as_view(), name='my-teams'),

                  path('', TeamAPIView.as_view(), name='team_list'),
                 # path('search/', SearchFilterView.as_view(), name='searxh'),
                  url(r'^(?P<pk>[\w-]+)/update/$', TeamUpdateAPIView.as_view(), name='update_team'),
                  url(r'^(?P<pk>[\w-]+)/leave/$', LeaveTeamListAPIView.as_view(), name='leave-team'),
                  url(r'^(?P<pk>[\w-]+)/detail/$', TeamDetailsAPIView.as_view(), name='team_details'),
                  url(r'^invitation/(?P<pk>[\w-]+)/action/$', MyTeamInviteActionAPIView.as_view(),
                      name='action-team-invitation'),
                  url(r'^banned/list/$', BannedListAPIView.as_view(), name='list_banned'),
                  url(r'^banned/(?P<pk>[\w-]+)/remove/$', BanRemoveAPIView.as_view(), name='remove_banned'),
                  url(r'^(?P<pk>[\w-]+)/delete/$', TeamDeleteAPIView.as_view(), name='team-delete'),
                  url(r'^preference/create/$', TeamPreferenceCreateAPIView.as_view(), name='team-preference-create'),
                  url(r'^preference/(?P<team>[\w-]+)/update/$', TeamPreferenceUpdateAPIView.as_view(), name='team-delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
