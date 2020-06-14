from django.shortcuts import render
from .models import Config
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.encoding import force_text
from django.views import View
from rest_framework import generics, mixins
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