# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models


from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        verbose_name_plural = "Users"


    def __str__(self):
         return self.username



class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'
        verbose_name_plural = "Categories"

    def __str__(self):
         return self.category_name

class Customers(models.Model):
    CUSTOMER_TYPES = [
        ('Regular', 'regular'),
        ('Walkin', 'walkin'),
    ]

    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    customer_type = models.CharField(max_length=7, choices=CUSTOMER_TYPES, default='regular')
    
    class Meta:
        managed = False
        db_table = 'customers'
        verbose_name_plural = "Customers"

    def __str__(self):
         return self.customer_name


class Discounts(models.Model):
    APPLIES_TO_CHOICES = [
        ('Item', 'items'),
        ('Category', 'category'),
        ('Customer', 'customer'),
        ('Order', 'order'),
    ]

    discount_id = models.AutoField(primary_key=True)
    discount_name = models.CharField(max_length=255)
    discount_desc = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField()
    applies_to = models.CharField(max_length=8, choices=APPLIES_TO_CHOICES, default='all')
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'discounts'
        verbose_name_plural = "Discounts"

    def __str__(self):
         return self.discount_name


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        

class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inventoryadjustments(models.Model):
    ADJUSTMENT_TYPE_CHOICES = [
        ('Addition', 'addition'),
        ('Deduction', 'deduction'),
        ('Damage', 'damage'),
        ('loss', 'loss'),
    ]

    Inventoryadjustments_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('Items', models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    adjustment_type = models.CharField(max_length=9, choices=ADJUSTMENT_TYPE_CHOICES, default='increase')
    quantity = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    adjustment_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Inventoryadjustments'
        verbose_name_plural = "Inventoryadjustments"       



class Items(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Good', 'good'),
        ('Service', 'service'),
    ]

    item_id = models.AutoField(primary_key=True)
    item_code = models.CharField(unique=True, max_length=100)
    item_name = models.CharField(max_length=255)
    sku = models.CharField(unique=True, max_length=100)
    category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
    item_type = models.CharField(max_length=7, choices=ITEM_TYPE_CHOICES, default='product')
    item_desc = models.TextField(blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey('Taxconfigurations', models.DO_NOTHING, blank=True, null=True)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'items'
        verbose_name_plural = "Items"

    def __str__(self):
         return self.item_name


class Pricelists(models.Model):
    pricelist_id = models.AutoField(primary_key=True)
    pricelist_name = models.CharField(max_length=255)
    pricelist_desc = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10)
    effective_date = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pricelists'
        verbose_name_plural = "Pricelists"

    def __str__(self):
         return self.pricelist_name



class Purchaseorders(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'pending'),
        ('Approved', 'approved'),
        ('Received', 'received'),
        ('Canceled', 'canceled'),
    ]

    purchaseorder_id = models.AutoField(primary_key=True)
    purchaseorder_number = models.CharField(db_column='purchaseorder__number', unique=True, max_length=100)  # Field renamed because it contained more than one '_' in a row.
    vendor = models.ForeignKey('Vendors', models.DO_NOTHING, blank=True, null=True)
    Purchaseorders_status = models.CharField(max_length=8, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Purchaseorders'
        verbose_name_plural = "Purchaseorders"

    def __str__(self):
         return self.purchaseorder_number


class Purchasereceipts(models.Model):
    RECEIPT_STATUS_CHOICES = [
        ('Complete', 'complete'),
        ('Partial', 'partial'),
        ('Rejected', 'rejected'),
    ]

    purchase_receipt_id = models.AutoField(primary_key=True)
    purchaseorder = models.ForeignKey(Purchaseorders, models.DO_NOTHING, blank=True, null=True)
    vendor = models.ForeignKey('Vendors', models.DO_NOTHING, blank=True, null=True)
    received_quantity = models.IntegerField()
    purchase_receipt_status = models.CharField(max_length=8, choices=RECEIPT_STATUS_CHOICES, default='pending')
    received_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Purchasereceipts'
        verbose_name_plural = "Purchasereceipts"



class SalesorderDiscounts(models.Model):
    salesorder_discount_id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('Salesorders', models.DO_NOTHING, blank=True, null=True)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesorder_discounts'
        unique_together = (('sales_order', 'discount'),)
        verbose_name_plural = "SalesorderDiscounts"


class Salesorders(models.Model):
    SALES_ORDER_STATUS_CHOICES = [
        ('Pending', 'pending'),
        ('Processed', 'processed'),
        ('Shipped', 'shipped'),
        ('Completed', 'completed'),
        ('Canceled', 'canceled'),
    ]

    sales_order_id = models.AutoField(primary_key=True)
    sales_order_number = models.CharField(unique=True, max_length=100)
    customer = models.ForeignKey('Customers', models.DO_NOTHING, blank=True, null=True)
    order_status = models.CharField(max_length=9, choices=SALES_ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Salesorders'
        verbose_name_plural = "Salesorders"

    def __str__(self):
         return self.sales_order_number


class Salesordertax(models.Model):
    salesorder_tax_id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey(Salesorders, models.DO_NOTHING, blank=True, null=True)
    tax = models.ForeignKey('Taxconfigurations', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesordertax'
        unique_together = (('sales_order', 'tax'),)
        verbose_name_plural = "Salesordertax"



class Shipments(models.Model):
    SHIPMENT_STATUS_CHOICES = [
        ('Shipped', 'shipped'),
        ('Intransit', 'intransit'),
        ('Delivered', 'delivered'),
    ]

    shipment_id = models.AutoField(primary_key=True)
    shipment_number = models.CharField(unique=True, max_length=100)
    sales_order = models.ForeignKey(Salesorders, models.DO_NOTHING, blank=True, null=True)
    shipments_status  = models.CharField(max_length=9, choices=SHIPMENT_STATUS_CHOICES, default='pending')
    shipping_date  = models.DateField(blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'shipments'
        verbose_name_plural = "Shipments"

    def __str__(self):
         return self.shipment_number


class StockItems(models.Model):
    stock_item_id = models.AutoField(primary_key=True)
    stock = models.ForeignKey('Stockmanagement', models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(Items, models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    safety_stock_level = models.IntegerField()
    last_restocked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_items'
        verbose_name_plural = "StockItems"



class Stockmanagement(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_code = models.CharField(max_length=255)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockmanagement'
        verbose_name_plural = "Stockmanagement"



class Taxconfigurations(models.Model):
    TAX_APPLIES_TO_CHOICES = [
        ('Sales', 'sales'),
        ('Purchase', 'purchase'),
        ('Both', 'both'),
    ]

    tax_id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=255)
    rate_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applies_to = models.CharField(max_length=9, choices=TAX_APPLIES_TO_CHOICES, default='all')
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'taxconfigurations'
        verbose_name_plural = "Taxconfigurations"
        
    def __str__(self):
         return self.tax_name


class Vendors(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=255)
    vendor_company_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_payables = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendors'
        verbose_name_plural = "Vendors"        

    def __str__(self):
         return self.vendor_name


class Warehouses(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouses'
        verbose_name_plural = "Warehouses"        

    def __str__(self):
         return self.warehouse_name
