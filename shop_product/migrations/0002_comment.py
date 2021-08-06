# Generated by Django 3.2.5 on 2021-07-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]
