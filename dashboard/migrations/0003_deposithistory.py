# Generated by Django 4.0.3 on 2022-05-09 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_assetbalance_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=255)),
                ('to', models.CharField(max_length=255)),
                ('chain', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'Deposit History',
            },
        ),
    ]