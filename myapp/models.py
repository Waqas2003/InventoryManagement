from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone   
from django.conf import settings

class Custom_User(AbstractUser):
    user_type = models.CharField(max_length= 25, choices=[('admin', 'Admin'),('manager', 'Manager'),('cashier','Cashier')], default='cashier')
    store = models.ForeignKey('store', on_delete=models.DO_NOTHING, null=True, blank=True)
    warehouse = models.ForeignKey('warehouses', on_delete=models.DO_NOTHING, null=True, blank=True)
    class Meta:
        db_table = 'custom_user' 

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
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True,  default=0)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
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
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.valid_until < today:
            self.is_active = False
        else:
            self.is_active = True  
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
        ('Loss', 'loss'), 
        ('Unsold_items','unsold_items')
    ]   
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('items', models.PROTECT)  
    sales_order_return = models.ForeignKey('sales_order_return', models.PROTECT,null=True,blank=True)
    adjustment_type = models.CharField(max_length=15, choices=adjustment_type_choices, default='return',blank=True, null=True)
    quantity = models.IntegerField()
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    store = models.ForeignKey('store', on_delete=models.CASCADE)
    adjustment_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:        
        db_table = 'inventory_adjustments'
        verbose_name_plural = "inventory_adjustments"       

class defective_stock(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    inventory_adjustment = models.ForeignKey('inventory_adjustments',on_delete=models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'defective_stock'
        verbose_name_plural = 'defective_stock'

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
    last_restocked_at = models.DateTimeField(null=True, blank=True)
    safety_stock_level = models.IntegerField(default=10) 
    
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
    id = models.AutoField(primary_key=True)
    purchase_order_number = models.CharField(unique=True, max_length=100)
    warehouse = models.ForeignKey('warehouses', on_delete=models.CASCADE, null=True)
    remarks= models.TextField(max_length=255, null= True, blank =True)
    vendor = models.ForeignKey('vendors', on_delete=models.CASCADE , null= True, blank= True)
    created_at = models.DateTimeField(default=timezone.now, blank = True, null= True)
    status = models.CharField(max_length=50, choices=[('pending','Pending'), ('processed','Processed'), ('received','Received')],default='pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(timezone.now, null = True, blank=True)
    
    class Meta:        
        db_table = 'purchase_orders'
        verbose_name_plural = "purchase_orders"

    def __str__(self):
        return self.purchase_order_number

class purchase_order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(items, on_delete=models.CASCADE, null= True, blank= True)
    quantity= models.PositiveIntegerField()
    purchase_order= models.ForeignKey(purchase_orders, models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now, blank = True, null= True)
    
    def __str__(self):
        return f"Order {self.purchase_order.id} - item {self.item.id}"
    
    class Meta:
        
        db_table = 'purchase_order_detail'
        verbose_name_plural = "purchase_order_detail"        

class purchase_order_return(models.Model):
    id = models.AutoField(primary_key=True)
    purchase_order = models.ForeignKey('purchase_orders',on_delete=models.CASCADE, null=True, blank=True,db_column="sales_order_id")
    vendor = models.ForeignKey('vendors',on_delete=models.CASCADE, null=True, blank=True, db_column="customer_id")
    total_refund_amount = models.DecimalField(max_digits=10,  decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True, db_column='created_by')

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
    created_at = models.DateTimeField(default=timezone.now,null=True,blank=True)
    
    class Meta:
        db_table = 'purchase_order_return_detail'
        verbose_name_plural = "purchase_order_return_detail"

class purchase_receipts(models.Model):
    receipt_status_choices = [
        ('Pending','pending'),
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
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    
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
        ('Shipped', 'shipped'),
        ('Delivered', 'delivered'),
        ('Canceled', 'canceled'),
    ]

    id = models.AutoField(primary_key=True)
    store = models.ForeignKey('store', on_delete=models.DO_NOTHING, blank= True, null= True)
    area = models.ForeignKey(area, on_delete=models.SET_NULL, blank=True, null=True)
    sales_order_number = models.CharField(unique=True, max_length=100)
    customer = models.ForeignKey('customers', models.DO_NOTHING, blank=True, null=True)
    order_status = models.CharField(max_length=9, choices=sales_order_status_choices, default='delivered')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)

    class Meta:        
        db_table = 'sales_orders'
        verbose_name_plural = "sales_orders"

    def __str__(self):
         return self.sales_order_number

class sales_order_return(models.Model):
    return_type_choices=[
        ('damage','damage'),
        ('return item','return'),
        ('loss','loss')
    ]
    id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('sales_orders',on_delete=models.CASCADE, null=True, blank=True,db_column="sales_order_id")
    # sales_order_detail = models.ForeignKey('sales_order_detail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")
    return_type = models.CharField(max_length=15,choices=return_type_choices,default='return')
    return_reason = models.TextField(blank=True, null=True)
    customer = models.ForeignKey('customers',on_delete=models.CASCADE, null=True, blank=True, db_column="customer_id")
    total_refund_amount = models.DecimalField(max_digits=10,  decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True, db_column='created_by')
    store = models.ForeignKey('store', on_delete=models.CASCADE)
    class Meta:        
        db_table = 'sales_order_return'
        verbose_name_plural = "sales_order_return"
          
        
class sales_order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(items, on_delete=models.CASCADE)
    sales_order = models.ForeignKey(sales_orders, on_delete=models.CASCADE)
    price_per_piece = models.IntegerField()
    quantity = models.IntegerField()
    discounted_price = models.IntegerField()
    price_after_discount = models.IntegerField()
    price_after_tax = models.IntegerField()
    tax_price = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return f"Order {self.sales_order.id} - Item {self.item.id}"
    
    class Meta:
        db_table = 'sales_order_details'
        verbose_name_plural = "sales_order_detail"        
        
class sales_order_return_detail(models.Model):
    id = models.AutoField(primary_key=True)
    return_sale = models.ForeignKey("sales_order_return",on_delete=models.CASCADE, db_column="return_sale_id")
    sales_order_detail = models.ForeignKey('sales_order_detail', on_delete=models.CASCADE, null=True, blank=True, db_column="sales_order_detail_id")    
    item = models.ForeignKey("items",on_delete=models.CASCADE, db_column="item_id" )
    return_quantity = models.IntegerField()
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now,null=True,blank=True)
    
    class Meta:
        db_table = 'sales_order_return_detail'
        verbose_name_plural = "sales_order_return_detail"
        
class store_return_to_warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    inventory_adjustments = models.ForeignKey('inventory_adjustments', on_delete= models.CASCADE)        
    warehouse = models.ForeignKey('warehouses', on_delete=models.CASCADE)
    store = models.ForeignKey('store',on_delete=models.CASCADE) 
    created_at = models.DateTimeField(timezone.now)
    
    class Meta: 
        db_table = 'store_return_to_warehouse'
        verbose_name_plural = 'sales_return_to_warehouse' 


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
    shipments_status  = models.CharField(max_length=9, choices=shipments_status_choices, default='Delivered')
    shipping_date  = models.DateField(blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    
    class Meta:        
        db_table = 'shipments'
        verbose_name_plural = "shipments"

    def __str__(self):
         return self.shipment_number


class stock_items(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey('store', models.DO_NOTHING, blank=True, null=True )
    item = models.ForeignKey(items, models.DO_NOTHING, blank=True, null=True, related_name='stock_items')
    quantity = models.IntegerField()
    safety_stock_level = models.IntegerField()
    last_restocked_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)

    class Meta:                 
        db_table = 'stock_items'
        verbose_name_plural = "stock_items"

    def __str__(self):
        return f" {self.item} in {self.store.store_location}"
    
class tax_configurations(models.Model):
    tax_applies_to_choices = [
        ('Sales', 'sales'),
        ('Purchase', 'purchase'),
        ('Both', 'both'),
    ]    
    id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=255)
    rate_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applies_to = models.CharField(max_length=9, choices=tax_applies_to_choices, default='sales')
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    
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
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)

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
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)

    class Meta:        
        db_table = 'warehouses'
        verbose_name_plural = "warehouses"        

    def __str__(self):
         return self.warehouse_name
     
class warehouse_stock(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(warehouses,on_delete=models.CASCADE)
    item = models.ForeignKey(items,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    safety_stock_level = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    class Meta:
        db_table = 'warehouse_stock'   
        verbose_name_plural = 'warehouse_stock'

class notification(models.Model):
    notification_type_choices = [
        ('store','Store'),
        ('warehouse','Warehouse')
    ]    
    id = models.AutoField(primary_key=True)
    item_choices = models.CharField(max_length=10, choices=  notification_type_choices, default= 'store')
    message = models.TextField(null=True,blank=2)
    item = models.ForeignKey('Items',on_delete=models.CASCADE, null = True, blank=True)
    warehouse = models.ForeignKey('warehouses', on_delete=models.CASCADE, null = True, blank=True)
    store = models.ForeignKey('store', on_delete=models.DO_NOTHING, null =True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)        

    class Meta:
        db_table = 'notification'
        verbose_name_plural = 'notification'
        
    def __str__(self):
        return f"Notification for {self.item.item_name}"    

class store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.TextField(null= True, blank = True)
    store_location = models.TextField( max_length=255 , null= True, blank=True)
    created_at = models.DateTimeField(default= timezone.now, blank=True, null= True)
    warehouse = models.ForeignKey(warehouses, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    class Meta:
        db_table = 'store'
        verbose_name_plural = 'store'
        
    def __str__(self):
        return self.store_location   
        
class request_note(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(store, on_delete=models.CASCADE)
    remarks= models.TextField(max_length=255, null= True, blank =True)
    created_at = models.DateTimeField(default=timezone.now, blank = True, null= True)
    status = models.CharField(max_length=50, choices=[('pending','Pending'), ('processed','Processed'), ('received','Received')],default='pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    class Meta:
        db_table = 'request_note'
        verbose_name_plural = 'request_note'
       
 
class request_note_detail(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(items, on_delete=models.CASCADE, null= True, blank= True)
    quantity= models.PositiveIntegerField()
    request_note= models.ForeignKey(request_note, models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    class Meta:
        db_table = 'request_note_detail'
        verbose_name_plural = 'request_note_detail'
  
class transfer_note(models.Model):
    id = models.AutoField(primary_key=True)
    request_note = models.ForeignKey(request_note, on_delete=models.CASCADE, null= True, blank= True)  
    warehouse = models.ForeignKey(warehouses, on_delete=models.CASCADE, null = True, blank=True) 
    status = models.CharField(max_length=20, choices=[
        ('dispatched',' Dispatched'),
        ('intransit','Intransit'),
        ('delivered', 'Delivered')
    ], default='dispatched')
    transferred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null= True, blank= True) 
    remarks = models.TextField(max_length=255, null= True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'transfer_note'
        verbose_name_plural = 'transfer_note'   

class transfer_note_detail(models.Model):
    id = models.AutoField(primary_key= True)
    item = models.ForeignKey('items',models.CASCADE)
    transfer_note = models.ForeignKey('transfer_note', models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'transfer_note_detail'
        verbose_name_plural = 'transfer_note_detail'   
        
class receive_note(models.Model):
    id = models.AutoField(primary_key=True)
    transfer_note = models.ForeignKey(transfer_note, on_delete=models.CASCADE, null=True, blank= True)
    store = models.ForeignKey(store, on_delete=models.CASCADE)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True, blank=True)    
    received_at=models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[('pending','Pending'), ('processed','Processed'), ('received','Received')],default='pending')
    warehouse = models.ForeignKey('warehouses', on_delete = models.DO_NOTHING, null = True, blank = True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'receive_note'
        verbose_name_plural= 'receive_note'    

class receive_note_detail(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('items' , on_delete=models.CASCADE)    
    receive_note = models.ForeignKey('receive_note', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'receive_note_detail'
        verbose_name_plural = 'receive_note_detail'           

class vendor_transfer_note(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_transfer_note_no = models.CharField(max_length=50, unique=True)
    purchase_order = models.ForeignKey('purchase_orders', on_delete= models.CASCADE)
    warehouse = models.ForeignKey(warehouses, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('dispatched','Dispatched'),('intransit', 'Intransit'),('delivered','Delivered')], default='dispatched')
    remarks = models.TextField(max_length=255, null=True, blank=True)
    vendor = models.ForeignKey('vendors',on_delete=models.CASCADE, null=True, blank=True )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta: 
        db_table = 'vendor_transfer_note'
        verbose_name_plural = 'vendor_transfer_note'    

    def __str__(self):
        return self.vendor_transfer_note_no

class vendor_transfer_note_detail(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_transfer_note =models.ForeignKey('vendor_transfer_note', on_delete=models.CASCADE)
    item = models.ForeignKey(items, on_delete=models.DO_NOTHING, null=True, blank=True)
    price_per_piece = models.IntegerField()
    quantity = models.IntegerField()    
     
    class Meta:
        db_table = 'vendor_transfer_note_detail'
        verbose_name_plural = 'vendor_transfer_note_detail'
    
class warehouse_receive_note(models.Model):
    id = models.AutoField(primary_key=True)
    receive_note_no = models.CharField(max_length=50, unique = True)
    vendor_transfer_note = models.ForeignKey(vendor_transfer_note, on_delete=models.CASCADE)
    received_at = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING, null=True, blank=True)
    warehouse = models.ForeignKey('warehouses',on_delete=models.CASCADE )
    status = models.CharField(max_length=50, choices=[('pending','Pending'), ('processed','Processed'), ('received','Received')],default='pending')  

    class Meta:
        db_table = 'warehouse_receive_note'
        verbose_name_plural = 'warehouse_receive_note'

    def __str__(self):
        return self.receive_note_no
    
class warehouse_receive_note_detail(models.Model):
    id = models.AutoField(primary_key= True)
    warehouse_receive_note = models.ForeignKey('warehouse_receive_note', on_delete=models.CASCADE)
    item= models.ForeignKey(items, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField()
        
    class Meta:
        db_table = 'warehouse_receive_note_detail'
        verbose_name_plural = 'warehouse_receive_note_detail'
    
    def __str__(self):
        return f"{self.quantity} of {self.item} received"
    
class vendor_bill(models.Model):
    id = models.AutoField(primary_key=True)
    bill_number = models.CharField(max_length=100, unique=True)
    vendor_transfer_note = models.ForeignKey(vendor_transfer_note, on_delete=models.CASCADE)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.PositiveIntegerField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid')
    ], default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    @property
    def remaining_balance(self):
        return self.net_amount - self.paid_amount
    
    class Meta:
        db_table = 'vendor_bill'
        verbose_name_plural = 'vendor_bill'
        
    def __str__(self):
        return self.bill_number    

class vendor_payment(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(vendor_bill, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        # ('bank', 'Bank Transfer'),
        # ('cheque', 'Cheque'),
        ('other', 'Other')
    ])
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'vendor_payment'
        verbose_name_plural = 'vendor_payment'