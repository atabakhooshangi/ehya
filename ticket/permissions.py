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


class IsExpert(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.role in ['3', '4']


def is_expert(request_user):
    """
    Allows access only to owner users.
    """
    return request_user.role.name in ['کارشناس', 'کارشناس ارشد']


class IsExpertOrIsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user == obj.user
