# Generated by Django 3.1.1 on 2020-10-25 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0003_auto_20201021_1805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wuzi',
            old_name='shangcijinhuo',
            new_name='jinhuoshijian',
        ),
        migrations.AlterUniqueTogether(
            name='wuzi',
            unique_together={('wuziming', 'jinhuoshijian')},
        ),
    ]
