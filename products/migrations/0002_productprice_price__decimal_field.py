# Generated by Django 3.2 on 2022-11-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
