from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    message = 'You Must Be SuperUser'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_staff
        )


class IsSuperUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_staff
        )


class IsSuperUserOrUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_staff or
            request.user.is_authenticated and obj == request.user
        )

class IsProfileOwnerOrSuperUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_staff or
            request.user.is_authenticated and obj.user == request.user
        )