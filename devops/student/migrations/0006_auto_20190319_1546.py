# Generated by Django 2.1.7 on 2019-03-19 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20190319_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='result',
            field=models.IntegerField(default=None),
        ),
    ]
