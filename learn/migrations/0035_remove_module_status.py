# Generated by Django 2.2.7 on 2019-11-25 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0034_auto_20190822_0450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='status',
        ),
    ]
