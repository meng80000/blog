# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20170711_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='site',
            field=models.CharField(max_length=32, unique=True, verbose_name='个人博客后缀'),
        ),
    ]