# Generated by Django 2.1.7 on 2019-03-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_testresult'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testresult',
            old_name='testId',
            new_name='testTakenId',
        ),
        migrations.AddField(
            model_name='testtaken',
            name='result',
            field=models.IntegerField(default=None),
        ),
    ]
