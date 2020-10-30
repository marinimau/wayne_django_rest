#
#   wayne_django_rest copyright © 2020 - all diricts reserved
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
from .models import SocialAccountUsername, SocialAccountEmail
from .permissions import SocialAccountListPermission, SocialAccountItemPermissions
from .serializers import SocialAccountUsernameSerializer, SocialAccountEmailSerializer


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
    permission_classes = [permissions.IsAuthenticated]


class UsernameSocialAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialAccountUsername.objects.all()
    serializer_class = SocialAccountUsernameSerializer
    permission_classes = [SocialAccountItemPermissions]


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


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------

@api_view()
def error_page(request):
    return Response({'detail': 'Not found'}, status=HTTP_404_NOT_FOUND)
