import django_filters
from vendor_app.models import PurchaseOrder
class PurchaseOrderFilter(django_filters.FilterSet):
    class Meta:
        model=PurchaseOrder
        fields=['vendor']