# Generated by Django 3.1.1 on 2020-11-05 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0017_faxing_faxingming'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tupian',
            name='lujing',
        ),
    ]