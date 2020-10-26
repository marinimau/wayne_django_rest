#
#   wayne_django_rest copyright © 2020 - all diricts reserved
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
    #   password reset
    # ------------------------------------------------------------------------------------------------------------------
    path('', views.ResetPasswordTokenList.as_view()),
    path('<int:pk>/', views.ResetPasswordTokenDetail.as_view()),
    path('confirm/', views.AlterPasswordByTokenAndEmail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)