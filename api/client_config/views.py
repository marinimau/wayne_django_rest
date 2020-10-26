#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from .models import Config
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from .serializers import ConfigSerializer
from .permissions import ConfigEditPermissions, ConfigListPermissions

# ----------------------------------------------------------------------------------------------------------------------
#   Config views
#   -   config_list
#       - if GET:   list all config object (superuser only)
#       - if POST:  not active
#   -   config_detail:
#       - if GET:   show config detail (owner or superuser)
#       - if PUT:   update config detail
#       - if DELETE: not active (delete the user instance for the configuration)
# ----------------------------------------------------------------------------------------------------------------------


class ConfigList(generics.ListCreateAPIView):
    queryset = Config.objects.all().order_by('user')
    serializer_class = ConfigSerializer
    permission_classes = [ConfigListPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [ConfigEditPermissions]


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------

@api_view()
def error_page(request):
    return Response({'detail': 'Not found'}, status=HTTP_404_NOT_FOUND)
