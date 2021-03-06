#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from contents.messages.get_messages import get_messages
from django.conf import settings
from .models import Profile
from .permissions import ProfileEditPermissions, UserEditPermissions, UserListPermissions, ProfileListPermissions
from .serializers import UserSerializer, ProfileSerializer
from .tokens import account_activation_token


messages = get_messages(package=settings.CONTENT_PACKAGES[0])


# ----------------------------------------------------------------------------------------------------------------------
#   Generic User views
#   -   user_list
#       - if GET:   list all user object
#       - if POST:  add new user
#   -   user_detail:
#       - if GET:   show user detail
#       - if PUT:   update user detail
#       - if DELETE: delete user
# ----------------------------------------------------------------------------------------------------------------------

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [UserListPermissions]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserEditPermissions]


# ----------------------------------------------------------------------------------------------------------------------
#   User Profile views
#   -   profile_list
#       - if GET:   list all profile object
#       - if POST:  add new profile
#   -   profile_detail:
#       - if GET:   show profile detail
#       - if PUT:   update profile detail
#       - if DELETE: delete profile
# ----------------------------------------------------------------------------------------------------------------------


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all().order_by('user')
    serializer_class = ProfileSerializer
    permission_classes = [ProfileListPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ProfileEditPermissions]


# ----------------------------------------------------------------------------------------------------------------------
#
#   Account activation
#
# ----------------------------------------------------------------------------------------------------------------------


class ActivateAccount(View):

    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            profile = Profile.objects.get(user=user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            profile = None
        if user is not None and profile is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            profile.email_confirmed = True
            user.save()
            msg = {'message': 'Account activated'}
            return render(request, 'account_activated.html', msg)
        else:
            msg = {'message': 'Invalid token'}
            return render(request, 'account_activated.html', msg)


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------

@api_view()
def error_page(request):
    return Response({'detail': messages['404_error']}, status=HTTP_404_NOT_FOUND)


# ----------------------------------------------------------------------------------------------------------------------
#
#   public
#
# ----------------------------------------------------------------------------------------------------------------------
class UserDetailPublic(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Restricts the returned accounts related to a given Wayne user,
        by filtering against a `username` query parameter in the URL.
        """
        username = self.kwargs['username']
        exists = User.objects.filter(username=username).exists()
        if exists:
            return User.objects.filter(username=username)
        else:
            return []


class ProfileDetailPublic(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Restricts the returned accounts related to a given Wayne user,
        by filtering against a `username` query parameter in the URL.
        """
        username = self.kwargs['username']
        exists = User.objects.filter(username=username).exists()
        if exists:
            return Profile.objects.filter(user=User.objects.get(username=username))
        else:
            return []
