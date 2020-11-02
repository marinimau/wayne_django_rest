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
#   Reset password token Permissions
#
# ----------------------------------------------------------------------------------------------------------------------

class ResetPasswordTokenListPermissions(permissions.BasePermission):
    """
    Custom permission to profile list
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_superuser
        else:
            return True


class ResetPasswordTokenSinglePermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
