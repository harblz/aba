# Generated by Django 2.2.3 on 2019-08-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0019_unit_unit_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_lessons',
            field=models.ManyToManyField(blank=True, null=True, to='learn.LessonPage'),
        ),
    ]
