# Generated by Django 3.1.3 on 2020-11-26 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20201126_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='warehouse',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
