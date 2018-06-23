# Generated by Django 2.0.4 on 2018-06-23 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_unit_unit_target'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50)),
                ('task_version', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='task_list_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Task'),
        ),
    ]
