from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, CategoriesViewSet, CustomersViewSet, DiscountsViewSet, InventoryadjustmentsViewSet, ItemsViewSet, PricelistsViewSet, PurchaseordersViewSet, PurchasereceiptsViewSet, SalesorderDiscountsViewSet, SalesordersViewSet, SalesordertaxViewSet, ShipmentsViewSet, StockItemsViewSet, StockmanagementViewSet, TaxconfigurationsViewSet, AuthUserViewSet, VendorsViewSet, WarehousesViewSet

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'customers', CustomersViewSet)
router.register(r'discounts', DiscountsViewSet)
router.register(r'inventoryadjustments', InventoryadjustmentsViewSet)
router.register(r'items', ItemsViewSet)
router.register(r'pricelists', PricelistsViewSet)
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

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]