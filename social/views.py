from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from .models import SocialLabel, SocialAccount
from .permissions import SocialLabelPermission, SocialLabelEditEditPermissions
from .serializers import LabelSerializer


# ----------------------------------------------------------------------------------------------------------------------
#   Generic Label views
#   -   label_list
#       - if GET:   list all labels object of a given user
#       - if POST:  add new label
#   -   label_detail:
#       - if GET:   show label detail
#       - if PUT:   update label detail
#       - if DELETE: delete label (if system == False)
# ----------------------------------------------------------------------------------------------------------------------

class LabelList(generics.ListCreateAPIView):
    queryset = SocialLabel.objects.all().order_by('title')
    serializer_class = LabelSerializer
    permission_classes = [SocialLabelPermission]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialLabel.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SocialLabelEditEditPermissions]


# ----------------------------------------------------------------------------------------------------------------------
#   Generic SocialAccount views
#   -   social_accounts_list
#       - if GET:   list all labels object of a given user
#       - if POST:  add new label
#   -   social_accounts_detail:
#       - if GET:   show user detail
#       - if PUT:   update user detail
#       - if DELETE: delete user
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#
#   404 error
#
# ----------------------------------------------------------------------------------------------------------------------

@api_view()
def error_page(request):
    return Response({'detail': 'Not found'}, status=HTTP_404_NOT_FOUND)