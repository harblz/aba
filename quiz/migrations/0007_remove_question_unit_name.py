# Generated by Django 2.0 on 2018-03-26 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20180325_0810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='unit_name',
        ),
    ]
