# Generated by Django 3.2.5 on 2021-08-01 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_product', '0014_product_sell'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartSell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('sell', models.IntegerField(default=0)),
                ('update', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pr_sell', to='shop_product.product')),
            ],
        ),
    ]
