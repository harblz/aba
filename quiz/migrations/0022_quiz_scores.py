# Generated by Django 2.1.3 on 2019-04-24 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0021_auto_20190313_0507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz_Scores',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Form')),
                ('unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Unit')),
            ],
        ),
    ]
