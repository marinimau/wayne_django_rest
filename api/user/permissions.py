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
#   User Permissions
#
# ----------------------------------------------------------------------------------------------------------------------


class UserListPermissions(permissions.BasePermission):
    """
    Custom permission to user_list
    """
    def has_permission(self, request, view):
        return request.user.is_superuser or request.method == 'POST'


class UserEditPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk or request.user.is_superuser


# ----------------------------------------------------------------------------------------------------------------------
#
#   Profile Permissions
#
# ----------------------------------------------------------------------------------------------------------------------

class ProfileListPermissions(permissions.BasePermission):
    """
    Custom permission to profile list
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        else:
            return request.user.is_superuser


class ProfileEditPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user or request.user.is_superuser




