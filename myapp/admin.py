from django.contrib import admin
from .models import defective_stock, store_return_to_warehouse, vendor_bill, vendor_payment, store, warehouse_stock, request_note,warehouse_receive_note, receive_note, transfer_note, categories, notification, sales_order_return,sales_order_return_detail, purchase_order_return_detail, sales_order_detail, purchase_order_return, area,purchase_order_detail, customers, discounts, inventory_adjustments, items, purchase_orders, purchase_receipts, Custom_User, sales_order_discounts, sales_orders, sales_order_tax,shipments, stock_items, tax_configurations,  vendors, warehouses
admin.site.register(categories)
admin.site.register(customers)
admin.site.register(discounts)
admin.site.register(inventory_adjustments)
admin.site.register(items)
admin.site.register(purchase_orders)
admin.site.register(purchase_order_detail)
admin.site.register(purchase_order_return)
admin.site.register(purchase_order_return_detail)
admin.site.register(purchase_receipts)
admin.site.register(sales_order_discounts)
# admin.site.register(sales_orders)
admin.site.register(sales_order_return)
admin.site.register(sales_order_tax)
admin.site.register(shipments)
admin.site.register(tax_configurations)
admin.site.register(vendors)
admin.site.register(warehouses)
admin.site.register(stock_items)
admin.site.register(warehouse_stock)
admin.site.register(Custom_User)
admin.site.register(area)
admin.site.register(sales_order_detail)
admin.site.register(sales_order_return_detail)
admin.site.register(notification)
admin.site.register(store)
admin.site.register(receive_note)
admin.site.register(request_note)
admin.site.register(transfer_note)
admin.site.register(warehouse_receive_note)
admin.site.register(vendor_payment)
admin.site.register(vendor_bill)
admin.site.register(store_return_to_warehouse)
admin.site.register(defective_stock)
# @admin.register(sales_orders)
# class SalesOrderAdmin(admin.ModelAdmin):
#     list_filter = ['created_at']