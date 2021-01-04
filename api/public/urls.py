#
#    copyright © 2020 - all rights reserved
#   Created at: 03/11/20
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.urls import path
from api.user import views as user_views
from api.social import views as social_views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   public urls
    # ------------------------------------------------------------------------------------------------------------------
    path('get/<username>/', user_views.UserDetailPublic.as_view()),
    path('get/<username>/detail/', user_views.ProfileDetailPublic.as_view()),
    path('get/<username>/account/username_based/', social_views.UsernameSocialAccountPublic.as_view()),
    path('reverse/username_based/<platform>/<value>/', social_views.UsernameSocialAccountRetrieve.as_view()),
    path('get/<username>/account/email_based/', social_views.EmailSocialAccountPublic.as_view()),
    path('reverse/email_based/<platform>/<value>/', social_views.EmailSocialAccountRetrieve.as_view()),

]
