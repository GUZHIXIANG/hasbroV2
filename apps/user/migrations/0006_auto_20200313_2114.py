# Generated by Django 2.2.7 on 2020-03-13 21:14

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '0001_squashed_0004_auto_20160611_1202'),
        ('wechat', '0002_auto_20200313_0950'),
        ('wechatapp', '0001_initial'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('xadmin', '0003_auto_20160715_0100'),
        ('user', '0005_usermanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserManager',
        ),
        migrations.CreateModel(
            name='UserManager',
            fields=[
            ],
            options={
                'verbose_name': '后台用户信息',
                'verbose_name_plural': '后台用户信息',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.userprofile',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]