from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsRoot(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser is True


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class WriteStaffReadAuth(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff


class IsReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated: return False
        return request.user.is_staff or request.user.type >= 1


class IsUser(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated: return False
        return not (request.user.is_staff or request.user.type >= 1)


class IsAuth(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
