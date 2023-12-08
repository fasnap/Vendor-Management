from django.urls import path
from .views import VendorListCreateAV,VendorDetailAV, PurchaseOrderListCreateAV, PurchaseOrderDetailAV, VendorPerformanceAV, PurchaseOrderAcknowledgeView

urlpatterns = [
    path('vendors/', VendorListCreateAV.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailAV.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderListCreateAV.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetailAV.as_view(), name='purchase-order-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAV.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge'),
]