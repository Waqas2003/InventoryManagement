# Generated by Django 5.1.5 on 2025-04-08 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_salesorder_return_price_per_piece_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salesorder_returndetail',
            options={'verbose_name_plural': 'salesorder_returndetail'},
        ),
        migrations.AlterField(
            model_name='inventoryadjustments',
            name='adjustment_type',
            field=models.CharField(blank=True, choices=[('Return', 'return'), ('Damage', 'damage'), ('loss', 'loss')], default='return', max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryadjustments',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='myapp.items'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventoryadjustments',
            name='salesorder_return',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='myapp.salesorder_return'),
        ),
        migrations.AlterField(
            model_name='salesorder_returndetail',
            name='price_per_piece',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='salesorder_returndetail',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterModelTable(
            name='salesorder_returndetail',
            table='salesorder_returndetail',
        ),
    ]
