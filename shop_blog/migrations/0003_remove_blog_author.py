# Generated by Django 3.2.5 on 2021-07-25 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0002_blog_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
    ]
