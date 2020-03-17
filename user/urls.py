from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   generic user urls
    # ------------------------------------------------------------------------------------------------------------------
    path('users/', views.UserList.as_view(), name='users-list'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   profile urls
    # ------------------------------------------------------------------------------------------------------------------
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   account activations urls
    # ------------------------------------------------------------------------------------------------------------------
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    # ------------------------------------------------------------------------------------------------------------------
    #   password reset
    # ------------------------------------------------------------------------------------------------------------------
    path('password_reset/', views.ResetPasswordTokenList.as_view()),
    path('password_reset/<int:pk>/', views.ResetPasswordTokenDetail.as_view()),
    path('password_reset/confirm/', views.AlterPasswordByTokenAndEmail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
