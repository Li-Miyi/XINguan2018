# Generated by Django 3.1.1 on 2020-10-30 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0009_auto_20201027_1441'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='lifashiqitadizhi',
            new_name='jishiqitadizhi',
        ),
        migrations.AlterField(
            model_name='pingjia',
            name='pingfen',
            field=models.IntegerField(default=5),
        ),
        migrations.DeleteModel(
            name='jixiaotongji',
        ),
    ]
