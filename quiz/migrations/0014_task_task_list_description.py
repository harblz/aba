# Generated by Django 2.0.4 on 2018-06-23 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_task_certification'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_list_description',
            field=models.CharField(default='Task Description', max_length=250),
            preserve_default=False,
        ),
    ]