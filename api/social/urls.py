#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import api.social.views as views

urlpatterns = [

    # ------------------------------------------------------------------------------------------------------------------
    #   social account based on username
    # ------------------------------------------------------------------------------------------------------------------
    path('username_based/', views.UsernameSocialAccountList.as_view()),
    path('username_based/<int:pk>', views.UsernameSocialAccountDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   social account based on email
    # ------------------------------------------------------------------------------------------------------------------
    path('email_based/', views.EmailSocialAccountList.as_view()),
    path('email_based/<int:pk>', views.EmailSocialAccountDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
