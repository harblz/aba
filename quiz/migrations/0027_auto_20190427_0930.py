# Generated by Django 2.1.3 on 2019-04-27 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0026_auto_20190427_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizscore',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
