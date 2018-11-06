"""SportActivities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

from PlayTheSport.SearchApi import SearchFilterView

urlpatterns = [
    url(r'^api/activity/', include(('ActivityApp.urls', 'activities'), namespace='ActivityApp')),
    url(r'^api/venue/', include(('VenueApp.urls', 'venues'), namespace='VenueApp')),
    url(r'^api/team/', include(('TeamApp.urls', 'Teams'), namespace='teams')),
    url(r'^api/profile/', include(('PlayerApp.urls', 'Profile'), namespace='profile')),
    url(r'^api/lookups/', include(('lookup.urls', 'lookups'), namespace='lookups')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    url(r'^api/profile/', include(('UserRegistrationApp.urls', 'profiles'), namespace='profiles')),
    path('api-auth', include('rest_framework.urls')),
    path('search/', SearchFilterView.as_view(), name='search'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    url(r'^auth/', include('djoser.urls')),
    # 'djoser.urls'
    #  -------------------------------------------------
    # user-me, password_reset, user-activate, set_password, api-root
    # user-change-username, password_reset_confirm, user-confirm, user,
    # root, user-list, user-delete, set_username, user-create
    #  -------------------------------------------------
    url(r'^auth/', include('djoser.urls.authtoken')),  # login, create token, destroy token , logout
    url(r'^auth/', include('djoser.urls.jwt')),  # jwt-create, jwt-verify, jwt-refresh
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

