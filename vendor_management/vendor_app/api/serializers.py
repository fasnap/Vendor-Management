from rest_framework import serializers
from vendor_app.models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields= '__all__'
        read_only_fields=['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields='__all__'
        read_only_fields = ('issue_date', 'acknowledgment_date')
        
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    on_time_delivery_rate=serializers.FloatField()
    quality_rating_avg=serializers.FloatField()
    average_response_time=serializers.FloatField()
    fulfillment_rate=serializers.FloatField()
    class Meta:
        model=HistoricalPerformance
        fields='__all__'
        
class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']
        
        