# Generated by Django 3.1.1 on 2020-10-26 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0005_auto_20201026_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wuzi',
            name='wuzileixing',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='wuzi',
            name='wuziming',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='wuzi',
            unique_together={('wuziming', 'wuzileixing')},
        ),
    ]