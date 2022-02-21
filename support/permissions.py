from rest_framework import permissions
from .models import SupportTicket

SupportAdminRoles = ['مدیر مطب',
                     'مدیر ارشد مطب',
                     'مدیر سایت',
                     'مدیر ارشد سایت',
                     'مدیر اپلیکیشن',
                     'مدیر ارشد اپلیکیشن',
                     'مدیر روابط عمومی',
                     'مدیر ارشد روابط عمومی',
                     'مدیر آموزش',
                     'مدیر ارشد آموزش']


class IsSupportAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj: SupportTicket):
        bool_list = []
        for role in request.user.role.all():
            if role in obj.section.associated_roles.all():
                bool_list.append('True')
        return 'True' in bool_list or request.user == obj.user
