# Generated by Django 2.1.7 on 2019-03-16 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20190316_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AddField(
            model_name='business',
            name='organization_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]
