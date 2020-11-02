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
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # If request is delete, only admin or owner can perform this operation
        if request.method == 'DELETE':
            return (obj.user == request.user or request.user.is_superuser) and not obj.required
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user or request.user.is_superuser
