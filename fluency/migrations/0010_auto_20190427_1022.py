# Generated by Django 2.1.3 on 2019-04-27 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluency', '0009_auto_20190427_1019'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FluencyTimedScores',
            new_name='FluencyTimedScore',
        ),
        migrations.RenameModel(
            old_name='FluencyUntimedScores',
            new_name='FluencyUntimedScore',
        ),
    ]
