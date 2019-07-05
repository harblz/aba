# Generated by Django 2.1.8 on 2019-06-30 21:37

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0029_quizscoresummary'),
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification_name', models.CharField(max_length=50)),
                ('certification_description', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objective_name', models.CharField(default='A', max_length=75)),
                ('objective_short_name', models.CharField(blank=True, max_length=75, null=True)),
                ('objective_description', ckeditor.fields.RichTextField(null=True)),
                ('objective_task_list_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_list_item_name', models.CharField(max_length=50)),
                ('task_list_item_description', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskListItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_list_item_category_name', models.CharField(max_length=50)),
                ('task_list_item_category_description', ckeditor.fields.RichTextField()),
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
            model_name='objective',
            name='objective_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Unit'),
        ),
    ]
