#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from contents.messages.get_messages import get_messages
from django.conf import settings
from api.user.models import User
from .models import SocialAccountUsername, SocialAccountEmail
from .permissions import SocialAccountListPermission, SocialAccountItemPermissions
from .serializers import SocialAccountUsernameSerializer, SocialAccountEmailSerializer


messages = get_messages(package=settings.CONTENT_PACKAGES[3])


# ----------------------------------------------------------------------------------------------------------------------
#   UsernameSocialAccount views
#   -   username_social_accounts_list
#       - if GET:   list all labels object of a given user
#       - if POST:  add new label
#   -   username_social_accounts_detail:
#       - if GET:   show user detail
#       - if PUT:   update user detail
#       - if DELETE: delete user
# ----------------------------------------------------------------------------------------------------------------------
class UsernameSocialAccountList(generics.ListCreateAPIView):
    queryset = SocialAccountUsername.objects.all()
    serializer_class = SocialAccountUsernameSerializer
    permission_classes = [permissions.IsAuthenticated, SocialAccountListPermission]


class UsernameSocialAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialAccountUsername.objects.all()
    serializer_class = SocialAccountUsernameSerializer
    permission_classes = [SocialAccountItemPermissions]


class UsernameSocialAccountPublic(generics.ListAPIView):
    serializer_class = SocialAccountUsernameSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user'

    def get_queryset(self):
        """
        Restricts the returned accounts related to a given Wayne user,
        by filtering against a `username` query parameter in the URL.
        """
        username = self.kwargs['username']
        exists = User.objects.filter(username=username).exists()
        if exists:
            return SocialAccountUsername.objects.filter(user=User.objects.get(username=username))
        else:
            return []


class UsernameSocialAccountRetrieve(generics.ListAPIView):
    serializer_class = SocialAccountUsernameSerializer
    permission_classes = [permissions.AllowAny]
    lookup_fields = ('platform', 'value')

    def get_queryset(self):
        platform = self.kwargs['platform']
        value = self.kwargs['value']
        exists = SocialAccountUsername.objects.filter(value=value).exists()
        if exists:
            return SocialAccountUsername.objects.filter(value=value).exists()
        else:
            return []


# ----------------------------------------------------------------------------------------------------------------------
#   EmailSocialAccount views
#   -   email_social_accounts_list
#       - if GET:   list all labels object of a given user
#       - if POST:  add new label
#   -   email_social_accounts_detail:
#       - if GET:   show user detail
#       - if PUT:   update user detail
#       - if DELETE: delete user
# ----------------------------------------------------------------------------------------------------------------------
class EmailSocialAccountList(generics.ListCreateAPIView):
    queryset = SocialAccountEmail.objects.all()
    serializer_class = SocialAccountEmailSerializer
    permission_classes = [permissions.IsAuthenticated, SocialAccountListPermission]


class EmailSocialAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialAccountEmail.objects.all()
    serializer_class = SocialAccountEmailSerializer
    permission_classes = [SocialAccountItemPermissions]


class EmailSocialAccountPublic(generics.ListAPIView):
    serializer_class = SocialAccountEmailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user'

    def get_queryset(self):
        """
        Restricts the returned accounts related to a given Wayne user,
        by filtering against a `username` query parameter in the URL.
        """
        username = self.kwargs['username']
        exists = User.objects.filter(username=username).exists()
        if exists:
            return SocialAccountEmail.objects.filter(user=User.objects.get(username=username))
        else:
            return []


class EmailSocialAccountRetrieve(generics.ListAPIView):
    serializer_class = SocialAccountEmailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_fields = ('platform', 'value')

    def get_queryset(self):
        platform = self.kwargs['platform']
        value = self.kwargs['value']
        exists = SocialAccountEmail.objects.filter(value=value, platform=platform).exists()
        if exists:
            return SocialAccountEmail.objects.filter(value=value, platform=platform).exists()
        else:
            return []


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------
@api_view()
def error_page(request):
    return Response({'detail': messages['404_error']}, status=HTTP_404_NOT_FOUND)
