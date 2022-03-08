from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext as _


class UserRoleFilter(admin.SimpleListFilter):
    title = _('نقش کاربری')
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(j, k)) for i, j, k in
             qs.values_list('role__id', 'role__name').annotate(
                 user_count=Count('role')).distinct().order_by(
                 'role__name')]
        t = ('all', f'همه ({qs.count()})')
        a.insert(0, t)
        if a[1][0] is None:
            a.pop(1)
        return a

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() and self.value() != 'all':  # Use the lookup id we sent above; to filter
            return queryset.filter(role=self.value())
        if self.value() == 'all':
            return queryset.all()


class UserActiveFilter(admin.SimpleListFilter):
    title = _('is active')
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format('بله' if j is True else 'نه', k)) for i, j, k in
             qs.values_list('is_active', 'is_active').annotate(
                 user_count=Count('is_active')).distinct().order_by(
                 '-is_active')]
        return a

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value():  # Use the lookup id we sent above; to filter
            return queryset.filter(is_active=self.value())

