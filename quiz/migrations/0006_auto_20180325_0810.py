# Generated by Django 2.0 on 2018-03-25 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20180325_0801'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='unit_id',
            new_name='unit',
        ),
    ]
