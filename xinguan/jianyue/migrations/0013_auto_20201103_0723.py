# Generated by Django 3.1.1 on 2020-11-03 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0012_auto_20201102_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tupian',
            name='url',
        ),
        migrations.AddField(
            model_name='tupian',
            name='src',
            field=models.ImageField(default=1, upload_to='img/'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='lifashizhuang',
        ),
    ]