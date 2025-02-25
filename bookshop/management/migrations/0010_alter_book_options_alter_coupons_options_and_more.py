# Generated by Django 5.1.6 on 2025-02-23 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_alter_order_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='coupons',
            options={'verbose_name': 'Coupon', 'verbose_name_plural': 'Coupons'},
        ),
        migrations.AlterModelOptions(
            name='orderitems',
            options={'verbose_name': 'Order item', 'verbose_name_plural': 'OrderItems'},
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('delivered', 'DELIVERED'), ('cancelled', 'CANCELLED')], default='pending', max_length=100),
        ),
    ]
