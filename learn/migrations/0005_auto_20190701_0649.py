# Generated by Django 2.1.8 on 2019-07-01 10:49

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0029_quizscoresummary'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0004_unit_unit_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', ckeditor.fields.RichTextField()),
                ('order', models.IntegerField()),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], max_length=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('page_views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Lesson Pages',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='course_units',
            field=models.ManyToManyField(to='quiz.Unit'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='objective_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Unit'),
        ),
        migrations.AddField(
            model_name='lessonpage',
            name='lesson_objectives',
            field=models.ManyToManyField(to='learn.Objective'),
        ),
        migrations.AddField(
            model_name='unit',
            name='unit_lessons',
            field=models.ManyToManyField(to='learn.LessonPage'),
        ),
    ]