# Generated by Django 3.2 on 2022-11-20 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_change_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='total_price',
        ),
    ]
