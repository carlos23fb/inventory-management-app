# Generated by Django 3.1.3 on 2020-12-04 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0022_auto_20201202_0106'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Categorie',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categorie',
        ),
    ]
