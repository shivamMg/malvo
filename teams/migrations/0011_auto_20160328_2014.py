# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-28 20:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20160327_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamCodingAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_no', models.IntegerField()),
                ('input_case_no', models.IntegerField()),
                ('answer_text', models.TextField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='teamcodinganswer',
            unique_together=set([('team', 'question_no', 'input_case_no')]),
        ),
    ]
