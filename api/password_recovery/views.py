#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from api.utils import get_client_ip
from .models import ResetPasswordToken
from .permissions import ResetPasswordTokenListPermissions, ResetPasswordTokenSinglePermissions
from .serializers import ResetPasswordTokenSerializer, AlterPasswordByTokenSerializer


# ----------------------------------------------------------------------------------------------------------------------
#
#   Password reset
#
# ----------------------------------------------------------------------------------------------------------------------

class ResetPasswordTokenList(generics.ListCreateAPIView):
    queryset = ResetPasswordToken.objects.all().order_by('user')
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


class AlterPasswordByTokenAndEmail(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Reset password
    """
    queryset = ResetPasswordToken.objects.all().order_by('user')
    serializer_class = AlterPasswordByTokenSerializer
    permission_classes = [ResetPasswordTokenListPermissions]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------

@api_view()
def error_page(request):
    return Response({'detail': 'Not found'}, status=HTTP_404_NOT_FOUND)
