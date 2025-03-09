# Generated by Django 5.1.5 on 2025-03-09 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('category_desc', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('billing_address', models.TextField(blank=True, null=True)),
                ('shipping_address', models.TextField(blank=True, null=True)),
                ('credit_limit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_bill', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('customer_type', models.CharField(choices=[('Regular', 'Regular'), ('Premium', 'Premium'), ('VIP', 'VIP')], max_length=25)),
            ],
            options={
                'verbose_name_plural': 'Customers',
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Discounts',
            fields=[
                ('discount_id', models.AutoField(primary_key=True, serialize=False)),
                ('discount_name', models.CharField(max_length=255)),
                ('discount_desc', models.TextField(blank=True, null=True)),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('valid_from', models.DateField()),
                ('valid_until', models.DateField()),
                ('applies_to', models.CharField(choices=[('ITEM', 'Item'), ('CATEGORY', 'Category'), ('Customer', 'Customer'), ('ORDER', 'Order')], max_length=10)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Discounts',
                'db_table': 'discounts',
            },
        ),
        migrations.CreateModel(
            name='Pricelists',
            fields=[
                ('pricelist_id', models.AutoField(primary_key=True, serialize=False)),
                ('pricelist_name', models.CharField(max_length=255)),
                ('pricelist_desc', models.TextField(blank=True, null=True)),
                ('currency', models.CharField(max_length=10)),
                ('effective_date', models.DateField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Pricelists',
                'db_table': 'pricelists',
            },
        ),
        migrations.CreateModel(
            name='Purchaseorders',
            fields=[
                ('purchaseorder_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchaseorder_number', models.CharField(db_column='purchaseorder__number', max_length=100, unique=True)),
                ('purchaseorders_status', models.CharField(blank=True, choices=[('Pending', 'pending'), ('Approved', 'approved'), ('Received', 'received'), ('Cancelled', 'cancelled')], max_length=25, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expected_delivery_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Purchaseorders',
                'db_table': 'purchaseorders',
            },
        ),
        migrations.CreateModel(
            name='Stockmanagement',
            fields=[
                ('stock_id', models.AutoField(primary_key=True, serialize=False)),
                ('stock_code', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Stockmanagement',
                'db_table': 'stockmanagement',
            },
        ),
        migrations.CreateModel(
            name='Taxconfigurations',
            fields=[
                ('tax_id', models.AutoField(primary_key=True, serialize=False)),
                ('tax_name', models.CharField(max_length=255)),
                ('rate_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('applies_to', models.CharField(choices=[('Sales', 'sales'), ('Purchases', 'purchases'), ('Both', 'both')], max_length=25)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Taxconfigurations',
                'db_table': 'taxconfigurations',
            },
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('vendor_id', models.AutoField(primary_key=True, serialize=False)),
                ('vendor_name', models.CharField(max_length=255)),
                ('vendor_company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('total_payables', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('credit_limit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
                'db_table': 'vendors',
            },
        ),
        migrations.CreateModel(
            name='Warehouses',
            fields=[
                ('warehouse_id', models.AutoField(primary_key=True, serialize=False)),
                ('warehouse_name', models.CharField(max_length=255)),
                ('warehouse_location', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Warehouses',
                'db_table': 'warehouses',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_code', models.CharField(max_length=100, unique=True)),
                ('item_name', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('item_type', models.CharField(choices=[('GOOD', 'good'), ('Service', 'service')], max_length=25)),
                ('item_desc', models.TextField(blank=True, null=True)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.categories')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.discounts')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.taxconfigurations')),
            ],
            options={
                'verbose_name_plural': 'Items',
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='Salesorders',
            fields=[
                ('sales_order_id', models.AutoField(primary_key=True, serialize=False)),
                ('sales_order_number', models.CharField(max_length=100, unique=True)),
                ('order_status', models.CharField(blank=True, choices=[('Pending', 'pending'), ('Shipped', 'shipped'), ('Delivered', 'delivered'), ('Canceled', 'canceled')], max_length=25, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('net_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.customers')),
            ],
            options={
                'verbose_name_plural': 'Salesorders',
                'db_table': 'salesorders',
            },
        ),
        migrations.CreateModel(
            name='Shipments',
            fields=[
                ('shipment_id', models.AutoField(primary_key=True, serialize=False)),
                ('shipment_number', models.CharField(max_length=100, unique=True)),
                ('carrier', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=255, null=True)),
                ('shipments_status', models.CharField(blank=True, choices=[('Shipped', 'shipped'), ('Delivered', 'delivered'), ('Cancelled', 'cancelled')], max_length=25, null=True)),
                ('shipping_date', models.DateField(blank=True, null=True)),
                ('expected_delivery_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('sales_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.salesorders')),
            ],
            options={
                'verbose_name_plural': 'Shipments',
                'db_table': 'shipments',
            },
        ),
        migrations.CreateModel(
            name='StockItems',
            fields=[
                ('stock_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('safety_stock_level', models.IntegerField()),
                ('last_restocked_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.items')),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.stockmanagement')),
            ],
            options={
                'verbose_name_plural': 'StockItems',
                'db_table': 'stock_items',
            },
        ),
        migrations.CreateModel(
            name='Purchasereceipts',
            fields=[
                ('purchase_receipt_id', models.AutoField(primary_key=True, serialize=False)),
                ('received_quantity', models.IntegerField()),
                ('purchase_receipt_status', models.CharField(blank=True, choices=[('Complete', 'complete'), ('Partial', 'partial'), ('Rejected', 'rejected')], max_length=25, null=True)),
                ('received_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('purchaseorder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.purchaseorders')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.vendors')),
            ],
            options={
                'verbose_name_plural': 'Purchasereceipts',
                'db_table': 'purchasereceipts',
            },
        ),
        migrations.AddField(
            model_name='purchaseorders',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.vendors'),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_password', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('user_type', models.CharField(choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Staff', 'Staff')], max_length=25)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.warehouses')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='stockmanagement',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.warehouses'),
        ),
        migrations.CreateModel(
            name='Inventoryadjustments',
            fields=[
                ('inventoryadjustments_id', models.AutoField(primary_key=True, serialize=False)),
                ('adjustment_type', models.CharField(choices=[('Addition', 'Addition'), ('Deduction', 'Deduction'), ('Damage', 'Damage'), ('Loss', 'Loss')], max_length=25)),
                ('quantity', models.IntegerField()),
                ('adjustment_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.items')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.users')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.warehouses')),
            ],
            options={
                'verbose_name_plural': 'Inventoryadjustments',
                'db_table': 'inventoryadjustments',
            },
        ),
        migrations.CreateModel(
            name='SalesorderDiscounts',
            fields=[
                ('salesorder_discount_id', models.AutoField(primary_key=True, serialize=False)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.discounts')),
                ('sales_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.salesorders')),
            ],
            options={
                'verbose_name_plural': 'SalesorderDiscounts',
                'db_table': 'salesorder_discounts',
                'unique_together': {('sales_order', 'discount')},
            },
        ),
        migrations.CreateModel(
            name='Salesordertax',
            fields=[
                ('salesorder_tax_id', models.AutoField(primary_key=True, serialize=False)),
                ('sales_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.salesorders')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.taxconfigurations')),
            ],
            options={
                'verbose_name_plural': 'Salesordertax',
                'db_table': 'salesordertax',
                'unique_together': {('sales_order', 'tax')},
            },
        ),
    ]
