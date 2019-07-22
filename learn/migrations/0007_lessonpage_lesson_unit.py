# Generated by Django 2.1.8 on 2019-07-05 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0029_quizscoresummary'),
        ('learn', '0006_auto_20190705_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonpage',
            name='lesson_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quiz.Unit'),
            preserve_default=False,
        ),
    ]
