# Generated by Django 2.1.7 on 2019-03-19 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0009_auto_20190316_1309'),
        ('business', '0003_auto_20190318_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Student')),
                ('testId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Test')),
            ],
        ),
    ]
