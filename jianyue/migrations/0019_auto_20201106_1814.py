# Generated by Django 3.1.1 on 2020-11-06 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0018_remove_tupian_lujing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tupian',
            name='tupianleixing',
            field=models.CharField(choices=[('0', '理发店'), ('1', '理发师'), ('2', '发型'), ('3', '用户')], max_length=1),
        ),
    ]
