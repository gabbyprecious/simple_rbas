from rest_framework import permissions


class OnlyStaffOwnerUserPermission(permissions.BasePermission):
    """
    Custom user API permissions.

    - Normal users can't send requests
    - Staff and Owner can do everything

    """

    message = 'Only Staff or Owner Users can access this endpoint.'

    def has_permission(self, request, view):
        allowed_level = {0, 2, 3,}
        return request.user.level in allowed_level


class OnlyAdminOwnerUserPermission(permissions.BasePermission):
    """
    Custom user API permissions.

    - Normal users can't send requests
    - Staff, Investor and Owner can do everything

    """

    message = 'Only Admin Staff or Owner Users can access this endpoint.'

    def has_permission(self, request, view):
        return request.user.level == 2 or request.user.level == 0


class OnlyInvestorOwnerUserPermission(permissions.BasePermission):
    """
    Custom user API permissions.

    - Normal users can't send requests
    - Investor and Owners can do everything

    """
    message = 'Only Investors or Owners can access this endpoint.'

    def has_permission(self, request, view):
        return request.user.level <= 1


class OnlyOwnerUserPermission(permissions.BasePermission):
    """
    Custom user API permissions.

    - Normal users can't send requests
    - Owners can do everything

    """

    message = 'Only Owners can access this endpoint.'

    def has_permission(self, request, view):
        return request.user.level == 0
