# Generated by Django 2.2.4 on 2019-10-20 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_remove_users_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(max_length=20, null=True, verbose_name='用户名'),
        ),
    ]
