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
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # If request is delete, only admin can perform this operation
        if request.method == 'DELETE':
            return request.user.is_superuser
        # Write permissions are only allowed to the owner of the snippet.
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
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # If request is delete, only admin can perform this operation
        if request.method == 'DELETE':
            return False
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user or request.user.is_superuser
