# Generated by Django 2.2.3 on 2019-08-22 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0031_auto_20190822_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='module_order',
            field=models.IntegerField(blank=True, help_text='Order left-to-right for published modules on the study page', null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='module_button',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
