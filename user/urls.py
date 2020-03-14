from django.urls import include, path
from rest_framework import routers
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
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),
    # ------------------------------------------------------------------------------------------------------------------
    #   profile urls
    # ------------------------------------------------------------------------------------------------------------------
    path('profiles/', views.profile_list),
    path('profiles/<int:pk>/', views.profile_detail),
]


