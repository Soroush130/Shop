# Generated by Django 3.2.5 on 2021-08-03 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_account', '0002_profile_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='job',
        ),
    ]