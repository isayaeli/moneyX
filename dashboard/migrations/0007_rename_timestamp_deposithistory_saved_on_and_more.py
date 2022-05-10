# Generated by Django 4.0.3 on 2022-05-10 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_saved_on_deposithistory_timestamp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposithistory',
            old_name='timestamp',
            new_name='saved_on',
        ),
        migrations.RemoveField(
            model_name='deposithistory',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='deposithistory',
            name='chain',
        ),
        migrations.RemoveField(
            model_name='deposithistory',
            name='to',
        ),
        migrations.AddField(
            model_name='deposithistory',
            name='history',
            field=models.JSONField(null=True),
        ),
    ]
