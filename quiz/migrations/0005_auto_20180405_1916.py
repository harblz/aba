# Generated by Django 2.0.4 on 2018-04-05 23:16

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_choice_is_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
