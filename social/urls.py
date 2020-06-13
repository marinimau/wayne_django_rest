from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   social labels of given user
    # ------------------------------------------------------------------------------------------------------------------
    path('labels/', views.LabelList.as_view()),
    path('labels/<int:pk>', views.LabelDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)