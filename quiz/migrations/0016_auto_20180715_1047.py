# Generated by Django 2.0.4 on 2018-07-15 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_auto_20180628_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(default='A', max_length=50)),
                ('form_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='form',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quiz.Form'),
            preserve_default=False,
        ),
    ]
