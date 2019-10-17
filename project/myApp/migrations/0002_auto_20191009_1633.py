# Generated by Django 2.2.4 on 2019-10-09 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inform',
            options={'verbose_name_plural': '通知管理'},
        ),
        migrations.AddField(
            model_name='users',
            name='user_id',
            field=models.IntegerField(default=1, verbose_name='用户id'),
        ),
        migrations.AlterField(
            model_name='inform',
            name='inform_id',
            field=models.IntegerField(default=1, verbose_name='通知id'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(default=1)),
                ('content', models.CharField(max_length=20)),
                ('isShow', models.BooleanField(default=True, verbose_name='是否显示')),
                ('creator_id', models.IntegerField(default=1, verbose_name='创建者id')),
                ('update_id', models.IntegerField(default=1, verbose_name='更新者id')),
                ('lastTime', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('isDel', models.BooleanField(default=True, verbose_name='是否删除')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Users')),
            ],
            options={
                'verbose_name_plural': '留言管理',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_id', models.IntegerField(verbose_name='收藏表')),
                ('creator_id', models.IntegerField(default=1, verbose_name='创建者id')),
                ('update_id', models.IntegerField(default=1, verbose_name='更新者id')),
                ('lastTime', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('isDel', models.BooleanField(default=True, verbose_name='是否删除')),
                ('inform_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Inform')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Users')),
            ],
            options={
                'verbose_name_plural': '收藏管理',
            },
        ),
    ]