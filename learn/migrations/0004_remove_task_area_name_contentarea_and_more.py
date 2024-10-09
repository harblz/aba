# Generated by Django 5.1.1 on 2024-10-06 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learn", "0003_alter_task_task_desc"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="area_name",
        ),
        migrations.CreateModel(
            name="ContentArea",
            fields=[
                (
                    "slug",
                    models.SlugField(primary_key=True, serialize=False, unique=True),
                ),
                ("letter", models.CharField(max_length=1)),
                ("section", models.IntegerField(blank=True, null=True)),
                ("area", models.CharField(max_length=50)),
                ("weight", models.IntegerField()),
                (
                    "license",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_areas",
                        to="learn.course",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="course",
            name="weights",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="learn.contentarea",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="area",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="learn.contentarea",
            ),
        ),
    ]