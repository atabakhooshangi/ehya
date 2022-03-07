from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext as _
from .models import EXPERT_STATUS_CHOICES


class TicketExpertStatusSerializer(admin.SimpleListFilter):
    title = _('وضعیت برای کارشناس')
    parameter_name = 'status_for_expert'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(EXPERT_STATUS_CHOICES[int(j) - 1][1], k)) for i, j, k in
             qs.values_list('status_for_expert', 'status_for_expert').annotate(
                 user_count=Count('status_for_expert')).distinct().order_by(
                 'status_for_expert')]
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
            return queryset.filter(status_for_expert=self.value())
        if self.value() == 'all':
            return queryset.all()


class TicketSectionFilter(admin.SimpleListFilter):
    title = _('بخش')
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(j, k)) for i, j, k in
             qs.values_list('section__id', 'section__name').annotate(
                 user_count=Count('section')).distinct().order_by(
                 'section__name')]
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
            return queryset.filter(section=self.value())
