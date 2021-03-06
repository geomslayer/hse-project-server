# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0005_auto_20170211_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('is_ans', models.BooleanField()),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.News')),
            ],
        ),
    ]
