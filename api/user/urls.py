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
