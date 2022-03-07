from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext as _
from . import models


class CommentApprovedFilter(admin.SimpleListFilter):
    title = _('تایید کامنت')
    parameter_name = 'approved'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format('تایید شده' if j is True else 'تایید نشده', k)) for i, j, k in
             qs.values_list('approved', 'approved').annotate(
                 user_count=Count('approved')).distinct().order_by(
                 '-approved')]
        t = ('all', f'همه ({qs.count()})')
        a.insert(0, t)
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
            return queryset.filter(approved=self.value())
        if self.value() == 'all':
            return queryset


class PostCategoryFilter(admin.SimpleListFilter):
    title = _('دسته بندی')
    parameter_name = 'categories'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(j, k)) for i, j, k in
             qs.values_list('categories__id', 'categories__name').annotate(
                 user_count=Count('categories')).distinct().order_by(
                 'categories__name')]
        t = ('all', f'همه ({qs.count()})')
        a.insert(0, t)
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
            return queryset.filter(categories=self.value())
        if self.value() == 'all':
            return queryset.all()


class InformsInfTypeSerializer(admin.SimpleListFilter):
    title = _('وضعیت انتشار')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(models.POST_STATUS[int(j) - 1][1], k)) for i, j, k in
             qs.values_list('status', 'status').annotate(
                 user_count=Count('status')).distinct().order_by(
                 'status')]
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
            return queryset.filter(status=self.value())

