# Generated by Django 3.1.1 on 2020-11-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0014_auto_20201103_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tupian',
            name='lifadian',
        ),
        migrations.AddField(
            model_name='tupian',
            name='tupianlaiyuan_id',
            field=models.CharField(default=1, max_length=700),
            preserve_default=False,
        ),
    ]
