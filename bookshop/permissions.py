from rest_framework.permissions import BasePermission, SAFE_METHODS

class CartPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "DELETE":
            return True
        else:
            return request.user.is_authenticated and request.user


class IsNotAuthenticated(BasePermission):
    message = "You cannot perform this action. You are already authenticated."
    def has_permission(self, request, view):
        return False if request.user.is_authenticated else True


class SessionPermission(BasePermission):
    message = "You did not attempt at registration."
    def has_permission(self, request, view):
        return True if request.session["user"] else False