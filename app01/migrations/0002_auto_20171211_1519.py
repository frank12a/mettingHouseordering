# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 07:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'verbose_name_plural': '预定情况'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name_plural': '会议室'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': '用户表'},
        ),
    ]
