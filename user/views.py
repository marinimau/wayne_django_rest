from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from rest_framework import generics
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST

from .models import Profile, ResetPasswordToken
from .permissions import ProfileEditPermissions, UserEditPermissions, UserListPermissions, ProfileListPermissions, \
    ResetPasswordTokenListPermissions, ResetPasswordTokenSinglePermissions
from .serializers import UserSerializer, ProfileSerializer, ResetPasswordTokenSerializer, AlterPasswordByToken
from rest_framework import permissions


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
from .tokens import account_activation_token
from .utils import get_client_ip


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
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
    queryset = Profile.objects.all()
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
    def get(request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            profile = Profile.objects.get(user=uid)
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
#   Password reset
#
# ----------------------------------------------------------------------------------------------------------------------

class ResetPasswordTokenList(generics.ListCreateAPIView):
    queryset = ResetPasswordToken.objects.all()
    serializer_class = ResetPasswordTokenSerializer
    permission_classes = [ResetPasswordTokenListPermissions]

    def perform_create(self, serializer):
        user_agent = self.request.META['HTTP_USER_AGENT']
        ip = get_client_ip(self.request)
        serializer.save(ip=ip, user_agent=user_agent)


class ResetPasswordTokenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResetPasswordToken.objects.all()
    serializer_class = ResetPasswordTokenSerializer
    permission_classes = [ResetPasswordTokenSinglePermissions]


class AlterPasswordByTokenAndEmail(generics.ListCreateAPIView):
    """
    Reset password
    """
    queryset = ResetPasswordToken.objects.all()
    serializer_class = AlterPasswordByToken
    permission_classes = [ResetPasswordTokenListPermissions]

