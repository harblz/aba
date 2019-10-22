# Generated by Django 2.2.3 on 2019-08-22 08:45

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0032_auto_20190822_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.CharField(default='module', max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')]),
        ),
    ]
