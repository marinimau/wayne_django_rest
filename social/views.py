from rest_framework import generics, permissions
from .models import SocialLabel, SocialAccount
from .permissions import SocialLabelPermission, SocialLabelEditEditPermissions


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
    serializer_class = UserSerializer
    permission_classes = [SocialLabelPermission]


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialLabel.objects.all()
    serializer_class = UserSerializer
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

