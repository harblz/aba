# Generated by Django 2.0.4 on 2018-06-23 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_auto_20180623_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='certification',
            field=models.CharField(default='RBT', max_length=25),
            preserve_default=False,
        ),
    ]
