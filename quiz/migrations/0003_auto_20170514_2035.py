# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 00:35
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0002_question_unit_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="question_hint",
            field=ckeditor.fields.CKEditor5Field(default="Think!"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="question",
            name="unit_name",
            field=models.CharField(max_length=50),
        ),
    ]
