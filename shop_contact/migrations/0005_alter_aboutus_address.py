# Generated by Django 3.2.5 on 2021-07-25 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_contact', '0004_alter_aboutus_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='address',
            field=models.CharField(max_length=500),
        ),
    ]
