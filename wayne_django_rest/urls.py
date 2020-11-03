"""wayne_django_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token
from api.user import views as user_views
from api.social import views as social_views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   admin urls
    # ------------------------------------------------------------------------------------------------------------------
    path('admin/', admin.site.urls),
    # ------------------------------------------------------------------------------------------------------------------
    #   auth urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/token-auth/', obtain_auth_token, name='api_token_auth'),
    # ------------------------------------------------------------------------------------------------------------------
    #   user urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/user/', include('api.user.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   password recovery
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/password_recovery/', include('api.password_recovery.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   config urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/config/', include('api.client_config.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   social urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/social/', include('api.social.urls')),
    # ------------------------------------------------------------------------------------------------------------------
    #   public urls
    # ------------------------------------------------------------------------------------------------------------------
    path('api/v1/public/<username>/', user_views.UserDetailPublic.as_view()),
    path('api/v1/public/<username>/detail/', user_views.ProfileDetailPublic.as_view()),
    path('api/v1/public/<username>/account/username_based/', social_views.UsernameSocialAccountPublic.as_view()),
    path('api/v1/public/<username>/account/email_based/', social_views.EmailSocialAccountPublic.as_view()),
]
