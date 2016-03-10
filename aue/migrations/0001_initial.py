# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-21 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[(b'0', b'INACTIVE'), (b'1', b'ACTIVE')], default=b'1', help_text=b'Category Status', max_length=2)),
                ('ip_address', models.CharField(blank=True, help_text=b'user ip address', max_length=128, null=True)),
                ('url', models.TextField(blank=True, help_text=b'searched URL', null=True)),
                ('goal', models.CharField(blank=True, help_text=b'User Goal', max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]