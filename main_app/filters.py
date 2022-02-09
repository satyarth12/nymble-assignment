from django_filters import FilterSet, DateTimeFilter
from .models import TransactionBill


class SalesFilter(FilterSet):
    from_date = DateTimeFilter(field_name='timestamp',
                               lookup_expr='gte')
    to_date = DateTimeFilter(field_name='timestamp',
                             lookup_expr='lte')

    class Meta:
        model = TransactionBill
        fields = (
            'from_date',
            'to_date'
        )
