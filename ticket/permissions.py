from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print(obj.user)
        return obj.user == request.user


def is_owner(obj, request_user):
    """
    Allows access only to owner users.
    """
    return obj.user == request_user
