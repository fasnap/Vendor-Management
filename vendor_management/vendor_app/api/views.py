from rest_framework import generics
from vendor_app.signals import update_metrics
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, PurchaseOrderAcknowledgeSerializer
from vendor_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from .filters import PurchaseOrderFilter
from django.utils import timezone

class VendorListCreateAV(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

class VendorDetailAV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    
class PurchaseOrderListCreateAV(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()
    filter_class=PurchaseOrderFilter
    
class PurchaseOrderDetailAV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()

class VendorPerformanceAV(generics.RetrieveAPIView):
    serializer_class=HistoricalPerformanceSerializer
    lookup_field = 'vendor_id'
    
    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        queryset = HistoricalPerformance.objects.filter(vendor_id=vendor_id)
        return queryset

class PurchaseOrderAcknowledgeView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderAcknowledgeSerializer
    
    def perform_update(self, serializer):
        instance = serializer.save(acknowledgment_date=timezone.now())
