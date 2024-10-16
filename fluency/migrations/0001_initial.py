# Generated by Django 2.1.3 on 2018-12-23 01:04

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', ckeditor.fields.RichTextField()),
                ('votes', models.IntegerField(default=0)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty_name', models.CharField(max_length=25)),
                ('difficulty_description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'Difficulties',
            },
        ),
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flashcard_text', ckeditor.fields.RichTextField()),
                ('Flashcard_hint', ckeditor.fields.RichTextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluency.Difficulty')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(default='A', max_length=75)),
                ('form_short_name', models.CharField(blank=True, max_length=75, null=True)),
                ('form_description', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50)),
                ('task_list_description', ckeditor.fields.RichTextField()),
                ('certification', models.CharField(default='RBT', max_length=25)),
                ('task_version', models.CharField(default='2017', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=50)),
                ('unit_description', ckeditor.fields.RichTextField()),
                ('unit_target', models.CharField(default='RBT', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='form_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluency.Unit'),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluency.Form'),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='task_list_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fluency.Task'),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluency.Unit'),
        ),
        migrations.AddField(
            model_name='choice',
            name='flashcard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluency.Flashcard'),
        ),
    ]
