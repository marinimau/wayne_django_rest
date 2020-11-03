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
    path('<username>/', user_views.UserDetailPublic.as_view()),
    path('<username>/detail/', user_views.ProfileDetailPublic.as_view()),
    path('<username>/account/username_based/', social_views.UsernameSocialAccountPublic.as_view()),
    path('<username>/account/email_based/', social_views.EmailSocialAccountPublic.as_view()),
]
