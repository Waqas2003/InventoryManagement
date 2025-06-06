# Generated by Django 5.1.5 on 2025-05-28 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_sales_orders_store_alter_notification_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='receive_note',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('received', 'Received')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='request_note',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('received', 'Received')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='transfer_note',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('delivered', 'Delivered')], default='pending', max_length=50),
        ),
    ]
