# Generated by Django 2.2.4 on 2019-12-19 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='title',
            field=models.CharField(default=1, max_length=1500, verbose_name='标题'),
        ),
    ]
