from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LoginView, CategoriesViewSet, CustomersViewSet,
    DiscountsViewSet,
    InventoryadjustmentsViewSet,
    ItemsViewSet,
    PurchaseordersViewSet,
    PurchasereceiptsViewSet,
    SalesorderDiscountsViewSet,
    SalesordersViewSet,
    SalesordertaxViewSet,
    ShipmentsViewSet,
    StockItemsViewSet,
    StockmanagementViewSet,
    TaxconfigurationsViewSet,
    AuthUserViewSet,
    VendorsViewSet,
    WarehousesViewSet,
    CustomTokenRefreshView,
    SalesReportView, PurchaseReportView,
    SalesOrderDetailViewSet,
    AreaViewSet,
    PlaceOrderViewSet,
    PurchaseOrder_returnViewSet,
    salesorder_returnViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'customers', CustomersViewSet)
router.register(r'discounts', DiscountsViewSet)
router.register(r'inventoryadjustments', InventoryadjustmentsViewSet)
router.register(r'items', ItemsViewSet)
router.register(r'purchaseorders', PurchaseordersViewSet)
router.register(r'purchasereceipts', PurchasereceiptsViewSet)
router.register(r'salesorderdiscounts', SalesorderDiscountsViewSet)
router.register(r'salesorders', SalesordersViewSet)
router.register(r'salesordertax', SalesordertaxViewSet)
router.register(r'shipments', ShipmentsViewSet)
router.register(r'stockitems', StockItemsViewSet)
router.register(r'stockmanagement', StockmanagementViewSet)
router.register(r'taxconfigurations', TaxconfigurationsViewSet)
router.register(r'users', AuthUserViewSet)
router.register(r'vendors', VendorsViewSet)
router.register(r'warehouses', WarehousesViewSet)
router.register(r'area', AreaViewSet)
router.register(r'salesorderdetail', SalesOrderDetailViewSet)
router.register(r'PurchaseOrder_return',PurchaseOrder_returnViewSet)
router.register(r'placeorder', PlaceOrderViewSet, basename='placeorder')
router.register(r'salesorder_return', salesorder_returnViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),  # Use the custom view
    path('login/', LoginView.as_view(), name='login'),
     path('reports/sales/', SalesReportView.as_view(), name='sales_report'),
    path('reports/purchases/', PurchaseReportView.as_view(), name='purchase_report'),
]
