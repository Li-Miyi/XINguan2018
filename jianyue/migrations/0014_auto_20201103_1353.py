# Generated by Django 3.1.1 on 2020-11-03 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0013_auto_20201103_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faxing',
            name='tupian',
        ),
        migrations.AddField(
            model_name='tupian',
            name='tupianleixing',
            field=models.CharField(choices=[('0', '理发店'), ('1', '理发师'), ('2', '发型')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]
