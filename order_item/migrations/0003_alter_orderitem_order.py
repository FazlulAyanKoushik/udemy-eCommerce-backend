# Generated by Django 4.1.5 on 2023-02-09 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_paidat_alter_order_deliveredat'),
        ('order_item', '0002_rename_product_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order'),
        ),
    ]
