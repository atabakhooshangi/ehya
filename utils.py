from django.db.models import Count
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext as _


class CustomSimpleListFilter(SimpleListFilter):
    def __init__(self, choice_tuple, has_all, request, params, model, model_admin):
        SimpleListFilter.__init__(self, request, params, model, model_admin)
        self.choice_tuple = choice_tuple
        self.has_all = has_all

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(self.choice_tuple[int(j) - 1][1], k)) for i, j, k in
             qs.values_list(f'{self.parameter_name}', f'{self.parameter_name}').annotate(
                 user_count=Count(f'{self.parameter_name}')).distinct().order_by(
                 f'{self.parameter_name}')]
        t = ('all', f'همه ({qs.count()})')
        if self.has_all:
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
        kwargs = {
            f'{self.parameter_name}': self.value()
        }
        if self.value() and self.value() != 'all':  # Use the lookup id we sent above; to filter
            return queryset.filter(**kwargs)
        if self.value() == 'all':
            return queryset.all()
