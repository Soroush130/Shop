# Generated by Django 3.2.5 on 2021-07-23 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_product', '0010_product_create_on'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop_cart', '0004_auto_20210723_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('create', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('f_name', models.CharField(max_length=300)),
                ('l_name', models.CharField(max_length=300)),
                ('phone', models.IntegerField(default=None)),
                ('address', models.CharField(max_length=700)),
                ('address_2', models.CharField(default=None, max_length=700)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='shop_cart.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='shop_product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
