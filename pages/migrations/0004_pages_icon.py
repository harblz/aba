# Generated by Django 2.0 on 2018-06-22 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_pages_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='icon',
            field=models.CharField(default='fas fa-home', max_length=50),
            preserve_default=False,
        ),
    ]
