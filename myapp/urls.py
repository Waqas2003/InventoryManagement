from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import (place_order,LoginView,DashboardView,categories_ViewSet,customers_ViewSet,discounts_ViewSet, inventory_adjustments_ViewSet, items_ViewSet,purchaseordersViewSet,purchase_receipts_ViewSet,sales_order_discounts_ViewSet,sales_orders_ViewSet,sales_order_tax_ViewSet,shipments_ViewSet,stock_items_ViewSet,stockmanagement_ViewSet,tax_configurations_ViewSet,AuthUser_ViewSet,vendors_ViewSet,warehouses_ViewSet,CustomTokenRefreshView,SalesReportView, PurchaseReportView,sales_order_detail_ViewSet,area_ViewSet,PlaceOrderViewSet,purchase_order_return_ViewSet,purchase_order_return_detail_ViewSet,sales_order_return_ViewSet,purchase_order_detail_ViewSet,notification_ViewSet)
from .views import (place_order, purchase_order_return_view, process_return, SalesReportView)



# router = DefaultRouter()
# router.register(r'categories', categories_ViewSet)
# router.register(r'customers', customers_ViewSet)
# router.register(r'discounts', discounts_ViewSet)
# router.register(r'inventoryadjustments', inventory_adjustments_ViewSet)
# router.register(r'items', items_ViewSet)
# router.register(r'purchaseorders', purchaseordersViewSet)
# router.register(r'purchase_order_detail', purchase_order_detail_ViewSet)
# router.register(r'purchase_order_return',purchase_order_return_ViewSet)
# router.register(r'PurchaseOrder_returndetail',purchase_order_return_detail_ViewSet)
# router.register(r'purchasereceipts', purchase_receipts_ViewSet)
# router.register(r'salesorderdiscounts', sales_order_discounts_ViewSet)
# router.register(r'salesorders', sales_orders_ViewSet)
# router.register(r'salesordertax', sales_order_tax_ViewSet)
# router.register(r'shipments', shipments_ViewSet)
# router.register(r'stockitems', stock_items_ViewSet)
# router.register(r'stockmanagement', stockmanagement_ViewSet)
# router.register(r'taxconfigurations', tax_configurations_ViewSet)
# router.register(r'users', AuthUser_ViewSet)
# router.register(r'vendors', vendors_ViewSet)
# router.register(r'warehouses', warehouses_ViewSet)
# router.register(r'area', area_ViewSet)
# router.register(r'salesorderdetail', sales_order_detail_ViewSet)
# router.register(r'placeorder', PlaceOrderViewSet, basename='placeorder')
# router.register(r'salesorder_return', sales_order_return_ViewSet)
# router.register(r'notification', notification_ViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), 
    # path('login/', LoginView.as_view(), name='login'),
    # path('reports/sales/', SalesReportView.as_view(), name='sales_report'),
    # path('reports/purchases/', PurchaseReportView.as_view(), name='purchase_report'),

    # path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    path('categories/', views.CategoriesListView.as_view(), name='categories_list'),
    path('categories/create/', views.CategoriesCreateView.as_view(), name='categories_create'),
    path('categories/<int:pk>/update/', views.CategoriesUpdateView.as_view(), name='categories_update'),
    path('categories/<int:pk>/delete/', views.CategoriesDeleteView.as_view(), name='categories_delete'),
    
    path('customers/', views.customersListView.as_view(), name='customers_list'),
    path('customers/create/', views.customersCreateView.as_view(), name='customers_create'),
    path('customers/<int:pk>/update/', views.customersUpdateView.as_view(), name='customers_update'),
    path('customers/<int:pk>/delete/', views.customersDeleteView.as_view(), name='customers_delete'),
    
    path('discounts/', views.discountsListView.as_view(), name='discounts_list'),
    path('discounts/create/', views.discountsCreateView.as_view(), name='discounts_create'),
    path('discounts/<int:pk>/update/', views.discountsUpdateView.as_view(), name='discounts_update'),
    path('discounts/<int:pk>/delete/', views.discountsDeleteView.as_view(), name='discounts_delete'),
    
    path('inventory_adjustments/', views.inventory_adjustmentsListView.as_view(), name='inventory_adjustments_list'),
    path('inventory_adjustments/create/', views.create_inventory_adjustment, name='inventory_adjustments_create'),
    path('inventory_adjustments/<int:pk>/update/', views.inventory_adjustmentsUpdateView.as_view(), name='inventory_adjustments_update'),
    path('inventory_adjustments/<int:pk>/delete/', views.inventory_adjustmentsDeleteView.as_view(), name='inventory_adjustments_delete'),
    
    path('purchase_orders/', views.purchase_ordersListView.as_view(), name='purchase_orders_list'),
    path('purchase_orders/create/', views.purchase_ordersCreateView.as_view(), name='purchase_orders_create'),
    path('purchase_orders/<int:pk>/update/', views.purchase_ordersUpdateView.as_view(), name='purchase_orders_update'),
    path('purchase_orders/<int:pk>/delete/', views.purchase_ordersDeleteView.as_view(), name='purchase_orders_delete'),
    
    path('purchase_order_detail/', views.purchase_order_detailListView.as_view(), name='purchase_order_detail_list'),
    path('purchase_order_detail/create/', views.purchase_order_detailCreateView.as_view(), name='purchase_order_detail_create'),
    path('purchase_order_detail/<int:pk>/update/', views.purchase_order_detailUpdateView.as_view(), name='purchase_order_detail_update'),
    path('purchase_order_detail/<int:pk>/delete/', views.purchase_order_detailDeleteView.as_view(), name='purchase_order_detail_delete'),
    
    path('purchase_order_return/', views.purchase_order_returnListView.as_view(), name='purchase_order_return_list'),
    path('purchase_order_return/create/', views.purchase_order_returnCreateView.as_view(), name='purchase_order_return_create'),
    path('purchase_order_return/<int:pk>/update/', views.purchase_order_returnUpdateView.as_view(), name='purchase_order_return_update'),
    path('purchase_order_return/<int:pk>/delete/', views.purchase_order_returnDeleteView.as_view(), name='purchase_order_return_delete'),
    
    path('purchase_order_return_detail/', views.purchase_order_return_detailListView.as_view(), name='purchase_order_return_detail_list'),
    path('purchase_order_return_detail/create/', views.purchase_order_return_detailCreateView.as_view(), name='purchase_order_return_detail_create'),
    path('purchase_order_return_detail/<int:pk>/update/', views.purchase_order_return_detailUpdateView.as_view(), name='purchase_order_return_detail_update'),
    path('purchase_order_return_detail/<int:pk>/delete/', views.purchase_order_return_detailDeleteView.as_view(), name='purchase_order_return_detail_delete'),
    
    path('purchase_receipts/', views.purchase_receiptsListView.as_view(), name='purchase_receipts_list'),
    path('purchase_receipts/create/', views.purchase_receiptsCreateView.as_view(), name='purchase_receipts_create'),
    path('purchase_receipts/<int:pk>/update/', views.purchase_receiptsUpdateView.as_view(), name='purchase_receipts_update'),
    path('purchase_receipts/<int:pk>/delete/', views.purchase_receiptsDeleteView.as_view(), name='purchase_receipts_delete'),
    
    path('sales_order_discounts/', views.sales_order_discountsListView.as_view(), name='sales_order_discounts_list'),
    path('sales_order_discounts/create/', views.sales_order_discountsCreateView.as_view(), name='sales_order_discounts_create'),
    path('sales_order_discounts/<int:pk>/update/', views.sales_order_discountsUpdateView.as_view(), name='sales_order_discounts_update'),
    path('sales_order_discounts/<int:pk>/delete/', views.sales_order_discountsDeleteView.as_view(), name='sales_order_discounts_delete'),
    
    path('area/', views.areaListView.as_view(), name='area_list'),
    path('area/create/', views.areaCreateView.as_view(), name='area_create'),
    path('area/<int:pk>/update/', views.areaUpdateView.as_view(), name='area_update'),
    path('area/<int:pk>/delete/', views.areaDeleteView.as_view(), name='area_delete'),
    
    path('sales_orders/', views.sales_ordersListView.as_view(), name='sales_orders_list'),
    path('sales_orders/create/', views.sales_ordersCreateView.as_view(), name='sales_orders_create'),
    path('sales_orders/<int:pk>/update/', views.sales_ordersUpdateView.as_view(), name='sales_orders_update'),
    path('sales_orders/<int:pk>/delete/', views.sales_ordersDeleteView.as_view(), name='sales_orders_delete'),
    
    path('sales_order_return/', views.sales_order_returnListView.as_view(), name='sales_order_return_list'),
    path('sales_order_return/create/', views.sales_order_returnCreateView.as_view(), name='sales_order_return_create'),
    path('sales_order_return/<int:pk>/update/', views.sales_order_returnUpdateView.as_view(), name='sales_order_return_update'),
    path('sales_order_return/<int:pk>/delete/', views.sales_order_returnDeleteView.as_view(), name='sales_order_return_delete'),
    
    path('sales_order_return_detail/', views.sales_order_return_detailListView.as_view(), name='sales_order_return_detail_list'),
    path('sales_order_return_detail/create/', views.sales_order_return_detailCreateView.as_view(), name='sales_order_return_detail_create'),
    path('sales_order_return_detail/<int:pk>/update/', views.sales_order_return_detailUpdateView.as_view(), name='sales_order_return_detail_update'),
    path('sales_order_return_detail/<int:pk>/delete/', views.sales_order_return_detailDeleteView.as_view(), name='sales_order_return_detail_delete'),
    
    path('sales_order_tax/', views.sales_order_taxListView.as_view(), name='sales_order_tax_list'),
    path('sales_order_tax/create/', views.sales_order_taxCreateView.as_view(), name='sales_order_tax_create'),
    path('sales_order_tax/<int:pk>/update/', views.sales_order_taxUpdateView.as_view(), name='sales_order_tax_update'),
    path('sales_order_tax/<int:pk>/delete/', views.sales_order_taxDeleteView.as_view(), name='sales_order_tax_delete'),
    
    path('shipments/', views.shipmentsListView.as_view(), name='shipments_list'),
    path('shipments/create/', views.shipmentsCreateView.as_view(), name='shipments_create'),
    path('shipments/<int:pk>/update/', views.shipmentsUpdateView.as_view(), name='shipments_update'),
    path('shipments/<int:pk>/delete/', views.shipmentsDeleteView.as_view(), name='shipments_delete'),
    
    path('stock_items/', views.stock_itemsListView.as_view(), name='stock_items_list'),
    path('stock_items/create/', views.stock_itemsCreateView.as_view(), name='stock_items_create'),
    path('stock_items/<int:pk>/update/', views.stock_itemsUpdateView.as_view(), name='stock_items_update'),
    path('stock_items/<int:pk>/delete/', views.stock_itemsDeleteView.as_view(), name='stock_items_delete'),
    
    path('stockmanagement/', views.stockmanagementListView.as_view(), name='stockmanagement_list'),
    path('stockmanagement/create/', views.stockmanagementCreateView.as_view(), name='stockmanagement_create'),
    path('stockmanagement/<int:pk>/update/', views.stockmanagementUpdateView.as_view(), name='stockmanagement_update'),
    path('stockmanagement/<int:pk>/delete/', views.stockmanagementDeleteView.as_view(), name='stockmanagement_delete'), 
    
    path('tax_configurations/', views.tax_configurationsListView.as_view(), name='tax_configurations_list'),
    path('tax_configurations/create/', views.tax_configurationsCreateView.as_view(), name='tax_configurations_create'),
    path('tax_configurations/<int:pk>/update/', views.tax_configurationsUpdateView.as_view(), name='tax_configurations_update'),
    path('tax_configurations/<int:pk>/delete/', views.tax_configurationsDeleteView.as_view(), name='tax_configurations_delete'),
    
    path('vendors/', views.vendorsListView.as_view(), name='vendors_list'),
    path('vendors/create/', views.vendorsCreateView.as_view(), name='vendors_create'),
    path('vendors/<int:pk>/update/', views.vendorsUpdateView.as_view(), name='vendors_update'),
    path('vendors/<int:pk>/delete/', views.vendorsDeleteView.as_view(), name='vendors_delete'),
    
    path('warehouses/', views.warehousesListView.as_view(), name='warehouses_list'),
    path('warehouses/create/', views.warehousesCreateView.as_view(), name='warehouses_create'),
    path('warehouses/<int:pk>/update/', views.warehousesUpdateView.as_view(), name='warehouses_update'),
    path('warehouses/<int:pk>/delete/', views.warehousesDeleteView.as_view(), name='warehouses_delete'),
    
    path('sales_order_detail/', views.sales_order_detailListView.as_view(), name='sales_order_detail_list'),
    path('sales_order_detail/create/', views.sales_order_detailCreateView.as_view(), name='sales_order_detail_create'),
    path('sales_order_detail/<int:pk>/update/', views.sales_order_detailUpdateView.as_view(), name='sales_order_detail_update'),
    path('sales_order_detail/<int:pk>/delete/', views.sales_order_detailDeleteView.as_view(), name='sales_order_detail_delete'),
    
    path('notification/', views.notificationListView.as_view(), name='notification_list'),
    path('notification/create/', views.notificationCreateView.as_view(), name='notification_create'),
    path('notification/<int:pk>/update/', views.notificationUpdateView.as_view(), name='notification_update'),
    path('notification/<int:pk>/delete/', views.notificationDeleteView.as_view(), name='notification_delete'),
            
    path('place_order/', place_order, name='place_order'),
    # path('order_success/', order_success, name='order_success'),
    path('purchase_return/', purchase_order_return_view, name='purchase_return'),

    path('create_purchase_order/', views.PurchaseOrderView.as_view(), name='create_purchase_order'),
    path('process_return/', process_return, name='process_return'),
    # path('sales-returns/', views.ProcessReturnView.as_view(), name='process_return'),

    # path('sales-summary/daily/', views.daily_sales_summary, name='daily_sales_summary'),
    # path('sales-summary/monthly/', views.monthly_sales_summary, name='monthly_sales_summary'),
    # path('sales-summary/yearly/', views.yearly_sales_summary, name='yearly_sales_summary'),
    
    # path('sales_summary/', views.sales_summary_view, name='sales_summary')
    path('sales_report/', SalesReportView.as_view(), name='sales_report'),
     path('sales_orders/<int:pk>/details/', views.sales_order_detail_view, name='sales_order_details'),



]
