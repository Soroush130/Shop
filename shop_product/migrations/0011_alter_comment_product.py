# Generated by Django 3.2.5 on 2021-07-25 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_product', '0010_product_create_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='co_pr', to='shop_product.product'),
        ),
    ]