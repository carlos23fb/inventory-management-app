# Generated by Django 3.1.3 on 2020-11-29 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_auto_20201127_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalorder',
            name='order_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]