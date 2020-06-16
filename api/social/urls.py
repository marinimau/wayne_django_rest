from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   social wall of given user
    # ------------------------------------------------------------------------------------------------------------------
    path('', views.WallList.as_view()),
    path('<int:pk>', views.WallDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   social labels of given user
    # ------------------------------------------------------------------------------------------------------------------
    path('labels/', views.LabelList.as_view()),
    path('labels/<int:pk>', views.LabelDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
