# Generated by Django 3.2.5 on 2021-08-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_product', '0018_slider_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='link',
            field=models.URLField(default=None),
        ),
    ]
