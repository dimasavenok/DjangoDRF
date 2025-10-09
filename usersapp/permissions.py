from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Разрешение для модераторов"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Разрешение только для владельцев объектов"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user