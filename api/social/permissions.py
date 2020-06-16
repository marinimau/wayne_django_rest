from rest_framework import permissions


# ----------------------------------------------------------------------------------------------------------------------
#
#   SocialWall Permissions
#
# ----------------------------------------------------------------------------------------------------------------------

class SocialWallPermission(permissions.BasePermission):
    """
    Custom permission to socialWall list
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_superuser
        return False


class SocialWallEditEditPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


# ----------------------------------------------------------------------------------------------------------------------
#
#   SocialLabel Permissions
#
# ----------------------------------------------------------------------------------------------------------------------

class SocialLabelPermission(permissions.BasePermission):
    """
    Custom permission to socialLabel list
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user is not None
        else:
            return request.user.is_superuser


class SocialLabelEditEditPermissions(permissions.BasePermission):
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
