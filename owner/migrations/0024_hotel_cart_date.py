# Generated by Django 5.1.3 on 2025-01-28 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0023_rename_order_master_bill_order_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel_cart',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
