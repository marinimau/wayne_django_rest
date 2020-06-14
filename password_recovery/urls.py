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