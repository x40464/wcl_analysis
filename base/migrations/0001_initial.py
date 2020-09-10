# Generated by Django 2.2.1 on 2020-08-27 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WCLLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='wcl log', max_length=100, verbose_name='标题')),
                ('code', models.CharField(default='wcl_code', max_length=50, verbose_name='wcl report code')),
                ('owner', models.CharField(default='xlinna', max_length=50, verbose_name='owner')),
                ('start', models.IntegerField(default=0, verbose_name='开始时间（timestamp毫秒）')),
                ('end', models.IntegerField(default=0, verbose_name='结束时间（timestamp毫秒）')),
                ('zone', models.IntegerField(default=0, verbose_name='区域')),
                ('parse_flag', models.BooleanField(default=False, verbose_name='日志解析状态')),
            ],
        ),
        migrations.CreateModel(
            name='Friendly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='xlinna', max_length=50, verbose_name='名称')),
                ('friendly_id', models.IntegerField(default=0)),
                ('guild', models.IntegerField(default=0)),
                ('type', models.CharField(blank=True, max_length=50, null=True, verbose_name='职业')),
                ('server', models.CharField(blank=True, max_length=50, null=True, verbose_name='服务器')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.WCLLog')),
            ],
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fight_id', models.IntegerField(default=0)),
                ('start', models.IntegerField(default=0, verbose_name='开始时间（timestamp毫秒）')),
                ('end', models.IntegerField(default=0, verbose_name='结束时间（timestamp毫秒）')),
                ('boss', models.IntegerField(default=0)),
                ('kill', models.BooleanField(default=True, verbose_name='是否击杀')),
                ('name', models.CharField(default="C'thun", max_length=50, verbose_name='名称')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.WCLLog')),
            ],
        ),
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enemy_id', models.IntegerField(default=0)),
                ('name', models.CharField(default="C'thun", max_length=50, verbose_name='名称')),
                ('guild', models.IntegerField(default=0)),
                ('type', models.CharField(blank=True, max_length=50, null=True, verbose_name='职业')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.WCLLog')),
            ],
        ),
    ]