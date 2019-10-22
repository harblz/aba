# Generated by Django 2.2.3 on 2019-08-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0028_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='pic',
            field=models.CharField(blank=True, help_text="This is the 'splash' picture that will be shown for the module. You can leave it blank. FOR PICS SERVED UP ON THE SITE, THEY SHOULD START WITH /static/img/", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='lessonpage',
            name='pic',
            field=models.CharField(blank=True, help_text="This is the 'splash' picture that will be shown for the unit. You can leave it blank. FOR PICS SERVED UP ON THE SITE, THEY SHOULD START WITH /static/img/", max_length=200, null=True),
        ),
    ]