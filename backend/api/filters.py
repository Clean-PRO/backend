from django_filters import rest_framework as filters

from services.models import Service


class FilterService(filters.FilterSet):
    """
    TODO: добавить docstring.
    """
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Service
        fields = ('title',)
