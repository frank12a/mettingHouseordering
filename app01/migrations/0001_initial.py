# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 04:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_id', models.IntegerField(choices=[(1, '8点到9点'), (2, '9点到10点'), (3, '10点到11点'), (4, '11点到12点'), (5, '14点到13点'), (6, '13点到14点'), (7, '14点到15点'), (8, '15点到16点'), (9, '16点到17点'), (10, '17点到18点')])),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='bookings',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Room'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Userinfo'),
        ),
        migrations.AlterUniqueTogether(
            name='bookings',
            unique_together=set([('room', 'user', 'time_id')]),
        ),
    ]
