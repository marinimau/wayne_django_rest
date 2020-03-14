from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # ------------------------------------------------------------------------------------------------------------------
    #   generic user urls
    # ------------------------------------------------------------------------------------------------------------------
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    # ------------------------------------------------------------------------------------------------------------------
    #   profile urls
    # ------------------------------------------------------------------------------------------------------------------
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


