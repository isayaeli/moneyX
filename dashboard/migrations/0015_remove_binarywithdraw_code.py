# Generated by Django 4.0.4 on 2022-06-04 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_binarywithdraw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='binarywithdraw',
            name='code',
        ),
    ]
