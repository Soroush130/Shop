# Generated by Django 3.2.5 on 2021-07-31 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
