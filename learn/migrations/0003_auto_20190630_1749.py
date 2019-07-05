# Generated by Django 2.1.8 on 2019-06-30 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0029_quizscoresummary'),
        ('learn', '0002_auto_20190630_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objective',
            name='objective_task_list_item',
        ),
        migrations.AddField(
            model_name='objective',
            name='objective_task_list_item',
            field=models.ManyToManyField(to='quiz.Task'),
        ),
    ]