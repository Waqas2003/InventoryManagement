# Generated by Django 5.1.5 on 2025-06-13 15:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_remove_vendor_payment_bill_delete_vendor_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendor_bill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bill_number', models.CharField(max_length=100, unique=True)),
                ('net_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partial', 'Partially Paid')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.discounts')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.tax_configurations')),
                ('vendor_transfer_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.vendor_transfer_note')),
            ],
            options={
                'verbose_name_plural': 'vendor_bill',
                'db_table': 'vendor_bill',
            },
        ),
        migrations.AddField(
            model_name='vendor_payment',
            name='bill',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.vendor_bill'),
            preserve_default=False,
        ),
    ]
