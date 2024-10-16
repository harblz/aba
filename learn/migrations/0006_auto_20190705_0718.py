# Generated by Django 2.1.8 on 2019-07-05 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_auto_20190701_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonpage',
            name='lesson_certification',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='learn.Certification'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lessonpage',
            name='lesson_course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='learn.Course'),
            preserve_default=False,
        ),
    ]
