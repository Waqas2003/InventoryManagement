from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LoginView, categories_ViewSet, customers_ViewSet,
    discounts_ViewSet,
    inventory_adjustments_ViewSet,
    items_ViewSet,
    purchaseordersViewSet,
    purchase_receipts_ViewSet,
    sales_order_discounts_ViewSet,
    sales_orders_ViewSet,
    sales_order_tax_ViewSet,
    shipments_ViewSet,
    stock_items_ViewSet,
    stockmanagement_ViewSet,
    tax_configurations_ViewSet,
    AuthUser_ViewSet,
    vendors_ViewSet,
    warehouses_ViewSet,
    CustomTokenRefreshView,
    SalesReportView, PurchaseReportView,
    sales_order_detail_ViewSet,
    area_ViewSet,
    PlaceOrderViewSet,
    purchase_order_return_ViewSet,
    purchase_order_return_detail_ViewSet,
    sales_order_return_ViewSet,
    purchase_order_detail_ViewSet,

)

router = DefaultRouter()
router.register(r'categories', categories_ViewSet)
router.register(r'customers', customers_ViewSet)
router.register(r'discounts', discounts_ViewSet)
router.register(r'inventoryadjustments', inventory_adjustments_ViewSet)
router.register(r'items', items_ViewSet)
router.register(r'purchaseorders', purchaseordersViewSet)
router.register(r'purchase_order_detail', purchase_order_detail_ViewSet)
router.register(r'purchase_order_return',purchase_order_return_ViewSet)
router.register(r'PurchaseOrder_returndetail',purchase_order_return_detail_ViewSet)
router.register(r'purchasereceipts', purchase_receipts_ViewSet)
router.register(r'salesorderdiscounts', sales_order_discounts_ViewSet)
router.register(r'salesorders', sales_orders_ViewSet)
router.register(r'salesordertax', sales_order_tax_ViewSet)
router.register(r'shipments', shipments_ViewSet)
router.register(r'stockitems', stock_items_ViewSet)
router.register(r'stockmanagement', stockmanagement_ViewSet)
router.register(r'taxconfigurations', tax_configurations_ViewSet)
router.register(r'users', AuthUser_ViewSet)
router.register(r'vendors', vendors_ViewSet)
router.register(r'warehouses', warehouses_ViewSet)
router.register(r'area', area_ViewSet)
router.register(r'salesorderdetail', sales_order_detail_ViewSet)
router.register(r'placeorder', PlaceOrderViewSet, basename='placeorder')
router.register(r'salesorder_return', sales_order_return_ViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), 
    path('login/', LoginView.as_view(), name='login'),
     path('reports/sales/', SalesReportView.as_view(), name='sales_report'),
    path('reports/purchases/', PurchaseReportView.as_view(), name='purchase_report'),
]
