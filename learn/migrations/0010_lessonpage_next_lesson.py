# Generated by Django 2.2.3 on 2019-08-06 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0009_auto_20190721_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonpage',
            name='next_lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='learn.LessonPage'),
            preserve_default=False,
        ),
    ]
