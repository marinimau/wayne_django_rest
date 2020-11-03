#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import permissions


# ----------------------------------------------------------------------------------------------------------------------
#
#   SocialAccount Permissions
#
# ----------------------------------------------------------------------------------------------------------------------

class SocialAccountListPermission(permissions.BasePermission):
    """
    Custom permission to SocialAccount list
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_superuser
        return request.user is not None


class SocialAccountItemPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
