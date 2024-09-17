# Generated by Django 5.1.1 on 2024-09-15 23:00

import django.core.validators
import re
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0035_remove_module_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonpage',
            name='slug',
            field=models.CharField(help_text="must be a single string, e.g. 'this-is-an-example'", max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='module',
            name='slug',
            field=models.CharField(default='module', max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
    ]