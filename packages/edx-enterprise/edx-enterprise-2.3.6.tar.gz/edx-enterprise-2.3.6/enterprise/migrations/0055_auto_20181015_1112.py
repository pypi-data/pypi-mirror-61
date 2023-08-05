# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-15 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0054_merge_20180914_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisecustomer',
            name='enable_autocohorting',
            field=models.BooleanField(default=False, help_text='Specifies whether the customer is able to assign learners to cohorts upon enrollment.'),
        ),
        migrations.AddField(
            model_name='historicalenterprisecustomer',
            name='enable_autocohorting',
            field=models.BooleanField(default=False, help_text='Specifies whether the customer is able to assign learners to cohorts upon enrollment.'),
        ),
    ]
