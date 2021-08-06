# Generated by Django 3.2.5 on 2021-07-20 13:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop_product', '0007_remove_product_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favourite',
            field=models.ManyToManyField(related_name='fa_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
