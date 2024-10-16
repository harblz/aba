# Generated by Django 2.2.3 on 2019-08-22 08:24

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0027_auto_20190821_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=50)),
                ('module_description', ckeditor.fields.RichTextField()),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], max_length=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('page_views', models.IntegerField(default=0)),
            ],
        ),
    ]
