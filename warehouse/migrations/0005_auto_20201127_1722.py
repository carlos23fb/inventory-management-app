# Generated by Django 3.1.3 on 2020-11-27 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20201126_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='orders',
        ),
        migrations.AddField(
            model_name='product',
            name='item_quantity',
            field=models.ManyToManyField(blank=True, related_name='items', to='warehouse.GeneralOrder'),
        ),
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.ManyToManyField(blank=True, related_name='orders', to='warehouse.GeneralOrder'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
