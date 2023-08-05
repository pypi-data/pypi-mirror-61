# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-06 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0005_party_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(choices=[('school', '\u5b66\u6821'), ('course', '\u8bfe\u7a0b'), ('exam', '\u6d4b\u9a8c')], db_index=True, max_length=64, verbose_name='\u540d\u5b57'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
