# from django.contrib.auth.models import User
# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone

# class categories(models.Model):
#     id = models.AutoField(primary_key=True)
#     category_name = models.CharField(max_length=255)
#     category_desc = models.TextField(blank=True, null=True)
#     parent = models.ForeignKey(
#         'self',  
#         on_delete=models.CASCADE,  
#         blank=True, 
#         null=True,
#         related_name='subcategories' 
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.category_name

#     class Meta:
        
#         db_table = 'categories'
#         verbose_name_plural = "Categories"

# class customers(models.Model):
#     customer_types = [
#         ('Regular', 'regular'),
#         ('Walkin', 'walkin'),
#     ]

#     id = models.AutoField(primary_key=True)
#     customer_name = models.CharField(max_length=255)
#     email = models.CharField(unique=True, max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     billing_address = models.TextField(blank=True, null=True)
#     shipping_address = models.TextField(blank=True, null=True)
#     credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     total_bill = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
#     created_at = models.DateTimeField(blank=True, null=True)
#     customer_type = models.CharField(max_length=7, choices=customer_types, default='regular')
    
#     class Meta:
        
#         db_table = 'customers'
#         verbose_name_plural = "customers"

#     def __str__(self):
#          return self.customer_name


# class discounts(models.Model):
#     applies_to_choices = [
#         ('Item', 'items'),
#         ('Category', 'category'),
#         ('Customer', 'customer'),
#         ('Order', 'order'),
#     ]

#     id = models.AutoField(primary_key=True)
#     discount_name = models.CharField(max_length=255)
#     discount_desc = models.TextField(blank=True, null=True)
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     valid_from = models.DateField()
#     valid_until = models.DateField()
#     applies_to = models.CharField(max_length=8, choices=APPLIES_TO_CHOICES, default='all')
#     created_at = models.DateTimeField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
    
#     def save(self, *args, **kwargs):
#         today = timezone.now().date()
#         if self.valid_until < today:
#             self.is_active = False
#         else:
#             self.is_active = True  # Force activate if date is valid
#         super().save(*args, **kwargs)
    
#     class Meta:
        
#         db_table = 'discounts'
#         verbose_name_plural = "discounts"

#     def __str__(self):
#          return self.discount_name


# class inventory_adjustments(models.Model):
#     adjustment_type_choices = [
#         ('Return', 'return'),
#         ('Damage', 'damage'),
#         ('loss', 'loss'),
#     ]   

#     id = models.AutoField(primary_key=True)
#     item = models.ForeignKey('Items', models.PROTECT)  
#     salesorder_return = models.ForeignKey('salesorder_return', models.PROTECT, default=1)
#     adjustment_type = models.CharField(max_length=9, choices=adjustment_type_choices, default='return',blank=True, null=True)
#     quantity = models.IntegerField()
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
#     adjustment_reason = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:        
#         db_table = 'Inventoryadjustments'
#         verbose_name_plural = "Inventoryadjustments"       


# class items(models.Model):
#     ITEM_TYPE_CHOICES = [
#         ('Good', 'good'),
#         ('Service', 'service'),
#     ]

#     id = models.AutoField(primary_key=True)
#     item_code = models.CharField(unique=True, max_length=100)
#     item_name = models.CharField(max_length=255)
#     sku = models.CharField(unique=True, max_length=100)
#     category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
#     item_type = models.CharField(max_length=7, choices=ITEM_TYPE_CHOICES, default='Good')  
#     item_desc = models.TextField(blank=True, null=True)
#     item_price = models.DecimalField(max_digits=10, decimal_places=2)
#     tax = models.ForeignKey('Taxconfigurations', models.DO_NOTHING, blank=True, null=True)
#     discount = models.ForeignKey('Discounts', models.DO_NOTHING, blank=True, null=True)
#     created_at = models.DateTimeField(default=timezone.now) 

   
#     parent = models.ForeignKey(
#         'self', 
#         on_delete=models.SET_NULL,  
#         blank=True,
#         null=True,
#         related_name="subitems"  
#     )
#     class Meta:
        
#         db_table = 'items'
#         verbose_name_plural = "Items"

#     def __str__(self):
#          return self.item_name

# class Purchaseorders(models.Model):
#     SALES_ORDER_STATUS_CHOICES = [
#         ('Pending', 'pending'),
#         ('Processed', 'processed'),
#         ('Shipped', 'shipped'),
#         ('Completed', 'completed'),
#         ('Canceled', 'canceled'),
#     ]

#     id = models.AutoField(primary_key=True)
#     purchaseorder_number = models.CharField(unique=True, max_length=100)
#     vendor = models.ForeignKey('Vendors', models.CASCADE, blank=True, null=True)
#     order_status = models.CharField(max_length=9, choices=SALES_ORDER_STATUS_CHOICES, default='pending')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
        
#         db_table = 'Purchaseorders'
#         verbose_name_plural = "Purchaseorders"

#     def __str__(self):
#         return self.purchaseorder_number

# class PurchaseOrderDetail(models.Model):
#     id = models.AutoField(primary_key=True)
#     item = models.ForeignKey(Items, on_delete=models.CASCADE)
#     purchase_order = models.ForeignKey(Purchaseorders, on_delete=models.CASCADE)
#     price_per_piece = models.IntegerField()
#     quantity = models.IntegerField()
#     discounted_price = models.IntegerField()
#     price_after_discount = models.IntegerField()
#     tax_price = models.IntegerField()
#     price_after_tax = models.IntegerField()
#     sub_total = models.IntegerField()
    
#     def __str__(self):
#         return f"Order {self.purchase_order.id} - Item {self.item.id}"
    
#     class Meta:
        
#         db_table = 'PurchaseOrderDetail'
#         verbose_name_plural = "PurchaseOrderDetail"        


# class PurchaseOrder_return(models.Model):
#     id = models.AutoField(primary_key=True)
#     purchaseorders = models.ForeignKey('Purchaseorders',on_delete=models.CASCADE, null=True, blank=True,db_column="sales_order_id")
#     # purchase_order_detail = models.ForeignKey('PurchaseOrderDetail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")
#     vendor = models.ForeignKey('Vendors',on_delete=models.CASCADE, null=True, blank=True, db_column="customer_id")
#     total_refund_amount = models.DecimalField(max_digits=10,  decimal_places=2)
#     created_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')

#     class Meta:        
#         db_table = 'PurchaseOrder_return'
#         verbose_name_plural = "PurchaseOrder_return"


# class PurchaseOrder_returndetail(models.Model):
#     id = models.AutoField(primary_key=True)
#     returnpurchase = models.ForeignKey("PurchaseOrder_return",on_delete=models.CASCADE, db_column="returnsale_id" )
#     purchase_order_detail = models.ForeignKey('PurchaseOrderDetail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")    
#     # item = models.ForeignKey("items",on_delete=models.CASCADE, db_column="item_id" )
#     return_quantity = models.IntegerField()
#     price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(null=True,blank=True)
    
#     class Meta:
#         db_table = 'PurchaseOrder_returndetail'
#         verbose_name_plural = "PurchaseOrder_returndetail"

# class Purchasereceipts(models.Model):
#     RECEIPT_STATUS_CHOICES = [
#         ('Complete', 'complete'),
#         ('Partial', 'partial'),
#         ('Rejected', 'rejected'),
#     ]

#     id = models.AutoField(primary_key=True)
#     purchaseorder = models.ForeignKey(Purchaseorders, models.DO_NOTHING, blank=True, null=True)
#     vendor = models.ForeignKey('Vendors', models.DO_NOTHING, blank=True, null=True)
#     received_quantity = models.IntegerField()
#     purchase_receipt_status = models.CharField(max_length=8, choices=RECEIPT_STATUS_CHOICES, default='pending')
#     received_date = models.DateField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
    
#     class Meta:        
#         db_table = 'Purchasereceipts'
#         verbose_name_plural = "Purchasereceipts"



# class SalesorderDiscounts(models.Model):
#     id = models.AutoField(primary_key=True)
#     sales_order = models.ForeignKey('Salesorders', models.DO_NOTHING, blank=True, null=True)
#     discount = models.ForeignKey(Discounts, models.DO_NOTHING, blank=True, null=True)

#     class Meta:        
#         db_table = 'salesorder_discounts'
#         unique_together = (('sales_order', 'discount'),)
#         verbose_name_plural = "SalesorderDiscounts"

# class Area(models.Model):
#     area_name = models.CharField(max_length=100)
#     delivery_charges = models.IntegerField()

#     def __str__(self):
#         return self.area_name
    
#     class Meta:        
#         db_table = 'area'
#         verbose_name_plural = "Area"         
    

# class Salesorders(models.Model):
#     SALES_ORDER_STATUS_CHOICES = [
#         ('Pending', 'pending'),
#         ('Processed', 'processed'),
#         ('Shipped', 'shipped'),
#         ('Completed', 'completed'),
#         ('Canceled', 'canceled'),
#     ]

#     id = models.AutoField(primary_key=True)
#     area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
#     sales_order_number = models.CharField(unique=True, max_length=100)
#     customer = models.ForeignKey('Customers', models.DO_NOTHING, blank=True, null=True)
#     order_status = models.CharField(max_length=9, choices=SALES_ORDER_STATUS_CHOICES, default='pending')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:        
#         db_table = 'Salesorders'
#         verbose_name_plural = "Salesorders"

#     def __str__(self):
#          return self.sales_order_number

# class salesorder_return(models.Model):
#     id = models.AutoField(primary_key=True)
#     sales_order = models.ForeignKey('Salesorders',on_delete=models.CASCADE, null=True, blank=True,db_column="sales_order_id")
#     sales_order_detail = models.ForeignKey('SalesOrderDetail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")
#     customer = models.ForeignKey('Customers',on_delete=models.CASCADE, null=True, blank=True, db_column="customer_id")
#     total_refund_amount = models.DecimalField(max_digits=10,  decimal_places=2)
#     created_at = models.DateTimeField(blank=True, null=True)
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')


#     class Meta:        
#         db_table = 'salesorder_return'
#         verbose_name_plural = "salesorder_return"

# class salesorder_returndetail(models.Model):
#     id = models.AutoField(primary_key=True)
#     returnsale = models.ForeignKey("salesorder_return",on_delete=models.CASCADE, db_column="returnsale_id" )
#     sales_order_detail = models.ForeignKey('SalesOrderDetail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")    
#     item = models.ForeignKey("items",on_delete=models.CASCADE, db_column="item_id" )
#     return_quantity = models.IntegerField()
#     price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(null=True,blank=True)
    
#     class Meta:
#         db_table = 'salesorder_returndetail'
#         verbose_name_plural = "salesorder_returndetail"
        



# class Salesordertax(models.Model):
#     id = models.AutoField(primary_key=True)
#     sales_order = models.ForeignKey('Salesorders', models.DO_NOTHING, blank=True, null=True)
#     tax = models.ForeignKey('Taxconfigurations', models.DO_NOTHING, blank=True, null=True)

#     class Meta:        
#         db_table = 'salesordertax'
#         unique_together = (('sales_order', 'tax'),)
#         verbose_name_plural = "Salesordertax"



# class Shipments(models.Model):
#     SHIPMENT_STATUS_CHOICES = [
#         ('Shipped', 'shipped'),
#         ('Intransit', 'intransit'),
#         ('Delivered', 'delivered'),
#     ]

#     id = models.AutoField(primary_key=True)
#     shipment_number = models.CharField(unique=True, max_length=100)
#     sales_order = models.ForeignKey(Salesorders, models.DO_NOTHING, blank=True, null=True)
#     shipments_status  = models.CharField(max_length=9, choices=SHIPMENT_STATUS_CHOICES, default='Intarnsit')
#     shipping_date  = models.DateField(blank=True, null=True)
#     expected_delivery_date = models.DateField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
    
#     class Meta:
        
#         db_table = 'shipments'
#         verbose_name_plural = "Shipments"

#     def __str__(self):
#          return self.shipment_number


# class StockItems(models.Model):
#     id = models.AutoField(primary_key=True)
#     stock = models.ForeignKey('Stockmanagement', models.DO_NOTHING, blank=True, null=True)
#     item = models.ForeignKey(Items, models.DO_NOTHING, blank=True, null=True, related_name='stock_items')
#     quantity = models.IntegerField()
#     safety_stock_level = models.IntegerField()
#     last_restocked_at = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:        
#         db_table = 'stock_items'
#         verbose_name_plural = "StockItems"


# class Stockmanagement(models.Model):
#     id = models.AutoField(primary_key=True)
#     stock_code = models.CharField(max_length=255)
#     warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
        
#         db_table = 'stockmanagement'
#         verbose_name_plural = "Stockmanagement"



# class Taxconfigurations(models.Model):
#     TAX_APPLIES_TO_CHOICES = [
#         ('Sales', 'sales'),
#         ('Purchase', 'purchase'),
#         ('Both', 'both'),
#     ]

#     id = models.AutoField(primary_key=True)
#     tax_name = models.CharField(max_length=255)
#     rate_percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     applies_to = models.CharField(max_length=9, choices=TAX_APPLIES_TO_CHOICES, default='all')
#     created_at = models.DateTimeField(blank=True, null=True)
    
#     class Meta:
        
#         db_table = 'taxconfigurations'
#         verbose_name_plural = "Taxconfigurations"
        
#     def __str__(self):
#          return self.tax_name


# class Vendors(models.Model):
#     id = models.AutoField(primary_key=True)
#     vendor_name = models.CharField(max_length=255)
#     vendor_company_name = models.CharField(max_length=255, blank=True, null=True)
#     email = models.CharField(unique=True, max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     total_payables = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
        
#         db_table = 'vendors'
#         verbose_name_plural = "Vendors"        

#     def __str__(self):
#          return self.vendor_name


# class Warehouses(models.Model):
#     id = models.AutoField(primary_key=True)
#     warehouse_name = models.CharField(max_length=255)
#     warehouse_location = models.CharField(max_length=255)
#     capacity = models.IntegerField()
#     created_at = models.DateTimeField(blank=True, null=True)
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

#     class Meta:
        
#         db_table = 'warehouses'
#         verbose_name_plural = "Warehouses"        

#     def __str__(self):
#          return self.warehouse_name

# class SalesOrderDetail(models.Model):
#     id = models.AutoField(primary_key=True)
#     item = models.ForeignKey(Items, on_delete=models.CASCADE)
#     sales_order = models.ForeignKey(Salesorders, on_delete=models.CASCADE)
#     price_per_piece = models.IntegerField()
#     quantity = models.IntegerField()
#     discounted_price = models.IntegerField()
#     price_after_discount = models.IntegerField()
#     tax_price = models.IntegerField()
#     price_after_tax = models.IntegerField()
#     sub_total = models.IntegerField()

#     def __str__(self):
#         return f"Order {self.sales_order.id} - Item {self.item.id}"
    
#     class Meta:
        
#         db_table = 'salesorderdetails'
#         verbose_name_plural = "SalesOrderDetail"        


from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_desc = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',  
        on_delete=models.CASCADE,  
        blank=True, 
        null=True,
        related_name='subcategories' 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        
        db_table = 'categories'
        verbose_name_plural = "Categories"

class customers(models.Model):
    customer_types = [
        ('Regular', 'regular'),
        ('Walkin', 'walkin'),
    ]

    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    customer_type = models.CharField(max_length=7, choices=customer_types, default='regular')
    
    class Meta:
        
        db_table = 'customers'
        verbose_name_plural = "customers"

    def __str__(self):
         return self.customer_name


class discounts(models.Model):
    applies_to_choices = [
        ('Item', 'items'),
        ('Category', 'category'),
        ('Customer', 'customer'),
        ('Order', 'order'),
    ]

    id = models.AutoField(primary_key=True)
    discount_name = models.CharField(max_length=255)
    discount_desc = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField()
    applies_to = models.CharField(max_length=8, choices=applies_to_choices, default='all')
    created_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.valid_until < today:
            self.is_active = False
        else:
            self.is_active = True  # Force activate if date is valid
        super().save(*args, **kwargs)
    
    class Meta:
        
        db_table = 'discounts'
        verbose_name_plural = "discounts"

    def __str__(self):
         return self.discount_name


class inventory_adjustments(models.Model):
    adjustment_type_choices = [
        ('Return', 'return'),
        ('Damage', 'damage'),
        ('loss', 'loss'),
    ]   

    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('items', models.PROTECT)  
    sales_order_return = models.ForeignKey('sales_order_return', models.PROTECT)
    adjustment_type = models.CharField(max_length=9, choices=adjustment_type_choices, default='return',blank=True, null=True)
    quantity = models.IntegerField()
    adjusted_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    adjustment_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:        
        db_table = 'inventory_adjustments'
        verbose_name_plural = "inventory_adjustments"       


class items(models.Model):
    item_type_choices = [
        ('Good', 'good'),
        ('Service', 'service'),
    ]

    id = models.AutoField(primary_key=True)
    item_code = models.CharField(unique=True, max_length=100)
    item_name = models.CharField(max_length=255)
    sku = models.CharField(unique=True, max_length=100)
    category = models.ForeignKey('categories', models.DO_NOTHING, blank=True, null=True)
    item_type = models.CharField(max_length=7, choices=item_type_choices, default='Good')  
    item_desc = models.TextField(blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey('tax_configurations', models.DO_NOTHING, blank=True, null=True)
    discount = models.ForeignKey('discounts', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now) 

   
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,  
        blank=True,
        null=True,
        related_name="subitems"  
    )
    class Meta:
        
        db_table = 'items'
        verbose_name_plural = "items"

    def __str__(self):
         return self.item_name

class purchase_orders(models.Model):
    sales_order_status_choices = [
        ('Pending', 'pending'),
        ('Processed', 'processed'),
        ('Shipped', 'shipped'),
        ('Completed', 'completed'),
        ('Canceled', 'canceled'),
    ]

    id = models.AutoField(primary_key=True)
    purchase_order_number = models.CharField(unique=True, max_length=100)
    vendor = models.ForeignKey('vendors', models.CASCADE, blank=True, null=True)
    order_status = models.CharField(max_length=9, choices=sales_order_status_choices, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:        
        db_table = 'purchase_orders'
        verbose_name_plural = "purchase_orders"

    def __str__(self):
        return self.purchase_order_number

class purchase_order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(items, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(purchase_orders, on_delete=models.CASCADE)
    price_per_piece = models.IntegerField()
    quantity = models.IntegerField()
    discounted_price = models.IntegerField()
    price_after_discount = models.IntegerField()
    tax_price = models.IntegerField()
    price_after_tax = models.IntegerField()
    sub_total = models.IntegerField()
    
    def __str__(self):
        return f"Order {self.purchase_order.id} - item {self.item.id}"
    
    class Meta:
        
        db_table = 'purchase_order_detail'
        verbose_name_plural = "purchase_order_detail"        


class purchase_order_return(models.Model):
    id = models.AutoField(primary_key=True)
    purchase_orders = models.ForeignKey('purchase_orders',on_delete=models.CASCADE, null=True, blank=True,db_column="sales_order_id")
    vendor = models.ForeignKey('vendors',on_delete=models.CASCADE, null=True, blank=True, db_column="customer_id")
    total_refund_amount = models.DecimalField(max_digits=10,  decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='created_by')

    class Meta:        
        db_table = 'purchase_order_return'
        verbose_name_plural = "purchase_order_return"


class purchase_order_return_detail(models.Model):
    id = models.AutoField(primary_key=True)
    return_purchase = models.ForeignKey("purchase_order_return",on_delete=models.CASCADE, db_column="return_purchase_id" )
    purchase_order_detail = models.ForeignKey('purchase_order_detail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")    
    return_quantity = models.IntegerField()
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(null=True,blank=True)
    
    class Meta:
        db_table = 'purchase_order_return_detail'
        verbose_name_plural = "purchase_order_return_detail"

class purchase_receipts(models.Model):
    receipt_status_choices = [
        ('Complete', 'complete'),
        ('Partial', 'partial'),
        ('Rejected', 'rejected'),
    ]

    id = models.AutoField(primary_key=True)
    purchase_order = models.ForeignKey(purchase_orders, models.DO_NOTHING, blank=True, null=True)
    vendor = models.ForeignKey('vendors', models.DO_NOTHING, blank=True, null=True)
    received_quantity = models.IntegerField()
    purchase_receipt_status = models.CharField(max_length=8, choices=receipt_status_choices, default='pending')
    received_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:        
        db_table = 'purchase_receipts'
        verbose_name_plural = "purchase_receipts"



class sales_order_discounts(models.Model):
    id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('sales_orders', models.DO_NOTHING, blank=True, null=True)
    discount = models.ForeignKey(discounts, models.DO_NOTHING, blank=True, null=True)

    class Meta:        
        db_table = 'sales_order_discounts'
        unique_together = (('sales_order', 'discount'),)
        verbose_name_plural = "sales_order_discounts"

class area(models.Model):
    area_name = models.CharField(max_length=100)
    delivery_charges = models.IntegerField()

    def __str__(self):
        return self.area_name
    
    class Meta:        
        db_table = 'area'
        verbose_name_plural = "area"         
    

class sales_orders(models.Model):
    sales_order_status_choices = [
        ('Pending', 'pending'),
        ('Processed', 'processed'),
        ('Shipped', 'shipped'),
        ('Completed', 'completed'),
        ('Canceled', 'canceled'),
    ]

    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(area, on_delete=models.CASCADE, blank=True, null=True)
    sales_order_number = models.CharField(unique=True, max_length=100)
    customer = models.ForeignKey('customers', models.DO_NOTHING, blank=True, null=True)
    order_status = models.CharField(max_length=9, choices=sales_order_status_choices, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:        
        db_table = 'sales_orders'
        verbose_name_plural = "sales_orders"

    def __str__(self):
         return self.sales_order_number

class sales_order_return(models.Model):
    id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('sales_orders',on_delete=models.CASCADE, null=True, blank=True,db_column="sales_order_id")
    sales_order_detail = models.ForeignKey('sales_order_detail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")
    customer = models.ForeignKey('customers',on_delete=models.CASCADE, null=True, blank=True, db_column="customer_id")
    total_refund_amount = models.DecimalField(max_digits=10,  decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='created_by')


    class Meta:        
        db_table = 'sales_order_return'
        verbose_name_plural = "sales_order_return"

class sales_order_return_detail(models.Model):
    id = models.AutoField(primary_key=True)
    return_sale = models.ForeignKey("sales_order_return",on_delete=models.CASCADE, db_column="return_sale_id" )
    sales_order_detail = models.ForeignKey('sales_order_detail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")    
    item = models.ForeignKey("items",on_delete=models.CASCADE, db_column="item_id" )
    return_quantity = models.IntegerField()
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(null=True,blank=True)
    
    class Meta:
        db_table = 'sales_order_return_detail'
        verbose_name_plural = "sales_order_return_detail"
        



class sales_order_tax(models.Model):
    id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('sales_orders', models.DO_NOTHING, blank=True, null=True)
    tax = models.ForeignKey('tax_configurations', models.DO_NOTHING, blank=True, null=True)

    class Meta:        
        db_table = 'sales_order_tax'
        unique_together = (('sales_order', 'tax'),)
        verbose_name_plural = "sales_order_tax"



class shipments(models.Model):
    shipments_status_choices = [
        ('Shipped', 'shipped'),
        ('Intransit', 'intransit'),
        ('Delivered', 'delivered'),
    ]

    id = models.AutoField(primary_key=True)
    shipment_number = models.CharField(unique=True, max_length=100)
    sales_order = models.ForeignKey(sales_orders, models.DO_NOTHING, blank=True, null=True)
    shipments_status  = models.CharField(max_length=9, choices=shipments_status_choices, default='Intarnsit')
    shipping_date  = models.DateField(blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        
        db_table = 'shipments'
        verbose_name_plural = "shipments"

    def __str__(self):
         return self.shipment_number


class stock_items(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey('stockmanagement', models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(items, models.DO_NOTHING, blank=True, null=True, related_name='stock_items')
    quantity = models.IntegerField()
    safety_stock_level = models.IntegerField()
    last_restocked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:        
        db_table = 'stock_items'
        verbose_name_plural = "stock_items"


class stockmanagement(models.Model):
    id = models.AutoField(primary_key=True)
    stock_code = models.CharField(max_length=255)
    warehouse = models.ForeignKey('warehouses', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'stockmanagement'
        verbose_name_plural = "stockmanagement"



class tax_configurations(models.Model):
    tax_applies_to_choices = [
        ('Sales', 'sales'),
        ('Purchase', 'purchase'),
        ('Both', 'both'),
    ]

    id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=255)
    rate_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applies_to = models.CharField(max_length=9, choices=tax_applies_to_choices, default='all')
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        
        db_table = 'tax_configurations'
        verbose_name_plural = "tax_configurations"
        
    def __str__(self):
         return self.tax_name


class vendors(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=255)
    vendor_company_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_payables = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'vendors'
        verbose_name_plural = "vendors"        

    def __str__(self):
         return self.vendor_name


class warehouses(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        
        db_table = 'warehouses'
        verbose_name_plural = "warehouses"        

    def __str__(self):
         return self.warehouse_name

class sales_order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(items, on_delete=models.CASCADE)
    sales_order = models.ForeignKey(sales_orders, on_delete=models.CASCADE)
    price_per_piece = models.IntegerField()
    quantity = models.IntegerField()
    discounted_price = models.IntegerField()
    price_after_discount = models.IntegerField()
    tax_price = models.IntegerField()
    price_after_tax = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return f"Order {self.sales_order.id} - Item {self.item.id}"
    
    class Meta:
        
        db_table = 'sales_order_details'
        verbose_name_plural = "sales_order_detail"        

