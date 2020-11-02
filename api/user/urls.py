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

from . import views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   generic user urls
    # ------------------------------------------------------------------------------------------------------------------
    path('', views.UserList.as_view(), name='users-list'),
    path('<int:pk>/', views.UserDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   profile urls
    # ------------------------------------------------------------------------------------------------------------------
    path('personal_data/', views.ProfileList.as_view()),
    path('personal_data/<int:pk>/', views.ProfileDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   account activations urls
    # ------------------------------------------------------------------------------------------------------------------
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
