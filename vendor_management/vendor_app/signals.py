from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance, Vendor
from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    vendor = instance.vendor 

    if instance.status == 'completed':
        # Calculate on_time_delivery_rate
        completed_po = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=instance.delivery_date).count()
        total_completed_po = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_delivery_rate = completed_po / total_completed_po if total_completed_po > 0 else 0.0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            defaults={'on_time_delivery_rate': on_time_delivery_rate, 'date': timezone.now()},
        )
        Vendor.objects.filter(pk=vendor.pk).update(on_time_delivery_rate=on_time_delivery_rate)

    if kwargs.get('created') and instance.quality_rating is not None:
        # Calculate quality_rating_avg
        po = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False)
        completed_po_count = po.count()
        total_quality_rating = sum(po.values_list('quality_rating', flat=True))
        avg_quality_rating = total_quality_rating / completed_po_count if completed_po_count > 0 else 0.0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            defaults={'quality_rating_avg': avg_quality_rating, 'date': timezone.now()},
        )
        Vendor.objects.filter(pk=vendor.pk).update(quality_rating_avg=avg_quality_rating)

    if instance.acknowledgment_date is not None:
        # Calculate average_response_time
        order_count = PurchaseOrder.objects.filter(vendor=vendor).count()
        po = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        total = sum((p.acknowledgment_date - p.issue_date).days for p in po)
        average_response_time = total / order_count if order_count > 0 else 0.0
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            defaults={'average_response_time': average_response_time, 'date': timezone.now()},
        )
        Vendor.objects.filter(pk=vendor.pk).update(average_response_time=average_response_time)

    # Calculate fulfillment_rate
    completed_po_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    total_po_count = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfillment_rate = completed_po_count / total_po_count if total_po_count > 0 else 0.0
    HistoricalPerformance.objects.update_or_create(
        vendor=vendor,
        defaults={'fulfillment_rate': fulfillment_rate, 'date': timezone.now()},
    )
    Vendor.objects.filter(pk=vendor.pk).update(fulfillment_rate=fulfillment_rate)
