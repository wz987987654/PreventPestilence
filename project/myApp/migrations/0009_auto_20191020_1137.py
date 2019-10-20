# Generated by Django 2.2.4 on 2019-10-20 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0008_auto_20191020_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='mail',
            new_name='user_mail',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='tele',
            new_name='user_phone',
        ),
        migrations.RemoveField(
            model_name='users',
            name='login_id',
        ),
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(default=1, max_length=20, verbose_name='用户名'),
        ),
    ]
