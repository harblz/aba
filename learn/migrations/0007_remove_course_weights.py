# Generated by Django 5.1.1 on 2024-10-06 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("learn", "0006_alter_course_weights"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="weights",
        ),
    ]
