# Generated by Django 2.1.7 on 2019-03-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20190316_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='organization_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='organization name'),
        ),
    ]
