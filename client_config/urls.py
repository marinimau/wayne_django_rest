from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   config urls
    # ------------------------------------------------------------------------------------------------------------------
    path('', views.ConfigList.as_view()),
    path('<int:pk>/', views.ConfigDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
