# Generated by Django 5.1.1 on 2024-10-06 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("learn", "0004_remove_task_area_name_contentarea_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="description",
        ),
    ]
