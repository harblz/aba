# Generated by Django 2.2.3 on 2019-08-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0030_auto_20190822_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='module_button',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
