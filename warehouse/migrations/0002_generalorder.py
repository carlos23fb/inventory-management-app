# Generated by Django 3.1.3 on 2020-11-26 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.PositiveIntegerField()),
                ('product', models.ManyToManyField(related_name='products', to='warehouse.Product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse')),
            ],
        ),
    ]
