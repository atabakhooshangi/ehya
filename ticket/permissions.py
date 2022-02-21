from rest_framework import permissions


class IsOwner(permissions.BasePermission):

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
        bool_list = []
        for role in request.user.role.all():
            if role.name in ['کارشناس', 'کارشناس ارشد']:
                bool_list.append('True')
        return 'True' in bool_list or request.user == obj.user


def per_checker(user, ls):
    bool_list = []
    for role in user.role.all():
        if role.name in ls:
            bool_list.append('True')
    return 'True' in bool_list


class IsTreasureAdminOrSeniorAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and per_checker(user=request.user,
                                                                           ls=['مدیر کل', 'مدیر گنجینه']) or bool(
                request.user and request.user.is_authenticated and request.user.is_superuser))
