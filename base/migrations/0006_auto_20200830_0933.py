# Generated by Django 2.2.1 on 2020-08-30 09:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20200830_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='wcllog',
            name='scan_flag',
            field=models.CharField(default='{}', max_length=1000),
        ),
        migrations.AlterField(
            model_name='wcllog',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 30, 9, 33, 47, 977445)),
        ),
    ]