# Generated by Django 3.1.1 on 2020-11-01 20:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0010_auto_20201031_0332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fuwu',
            name='pingjia',
        ),
        migrations.AddField(
            model_name='jishiqitadizhi',
            name='shenqingqingkuang',
            field=models.CharField(choices=[('1', '已批准'), ('0', '未批准')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jishiqitadizhi',
            name='shenqingshijian',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]