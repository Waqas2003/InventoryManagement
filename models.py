# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    customer_type = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'customers'


class Discounts(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_name = models.CharField(max_length=255)
    discount_desc = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField()
    applies_to = models.CharField(max_length=8)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discounts'


class Inventoryadjustments(models.Model):
    inventoryadjustments_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('Items', models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    adjustment_type = models.CharField(max_length=9)
    quantity = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    adjustment_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventoryadjustments'


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_code = models.CharField(unique=True, max_length=100)
    item_name = models.CharField(max_length=255)
    sku = models.CharField(unique=True, max_length=100)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    item_type = models.CharField(max_length=7)
    item_desc = models.TextField(blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey('Taxconfigurations', models.DO_NOTHING, blank=True, null=True)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'


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


class Purchaseorders(models.Model):
    purchaseorder_id = models.AutoField(primary_key=True)
    purchaseorder_number = models.CharField(db_column='purchaseorder__number', unique=True, max_length=100)  # Field renamed because it contained more than one '_' in a row.
    vendor = models.ForeignKey('Vendors', models.DO_NOTHING, blank=True, null=True)
    purchaseorders_status = models.CharField(max_length=8, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchaseorders'


class Purchasereceipts(models.Model):
    purchase_receipt_id = models.AutoField(primary_key=True)
    purchaseorder = models.ForeignKey(Purchaseorders, models.DO_NOTHING, blank=True, null=True)
    vendor = models.ForeignKey('Vendors', models.DO_NOTHING, blank=True, null=True)
    received_quantity = models.IntegerField()
    purchase_receipt_status = models.CharField(max_length=8, blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchasereceipts'


class SalesorderDiscounts(models.Model):
    salesorder_discount_id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('Salesorders', models.DO_NOTHING, blank=True, null=True)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesorder_discounts'
        unique_together = (('sales_order', 'discount'),)


class Salesorders(models.Model):
    sales_order_id = models.AutoField(primary_key=True)
    sales_order_number = models.CharField(unique=True, max_length=100)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    order_status = models.CharField(max_length=9, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesorders'


class Salesordertax(models.Model):
    salesorder_tax_id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey(Salesorders, models.DO_NOTHING, blank=True, null=True)
    tax = models.ForeignKey('Taxconfigurations', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesordertax'
        unique_together = (('sales_order', 'tax'),)


class Shipments(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    shipment_number = models.CharField(unique=True, max_length=100)
    sales_order = models.ForeignKey(Salesorders, models.DO_NOTHING, blank=True, null=True)
    carrier = models.CharField(max_length=255, blank=True, null=True)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    shipments_status = models.CharField(max_length=9, blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shipments'


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


class Stockmanagement(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_code = models.CharField(max_length=255)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockmanagement'


class Taxconfigurations(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=255)
    rate_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applies_to = models.CharField(max_length=9)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxconfigurations'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_password = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=8)
    created_at = models.DateTimeField(blank=True, null=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


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


class Warehouses(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouses'
