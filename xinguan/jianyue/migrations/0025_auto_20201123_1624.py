# Generated by Django 3.1.1 on 2020-11-23 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jianyue', '0024_dizhi_comprehension'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoucang',
            old_name='tupianleixing',
            new_name='shoucangleixing',
        ),
        migrations.AlterField(
            model_name='tupian',
            name='tupianleixing',
            field=models.CharField(choices=[('0', '理发店'), ('1', '理发师'), ('2', '发型'), ('3', '用户'), ('4', '资讯')], max_length=1),
        ),
        migrations.AlterUniqueTogether(
            name='shoucang',
            unique_together={('beishoucang_id', 'yonghu', 'shoucangleixing')},
        ),
        migrations.CreateModel(
            name='zixun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('neirong', models.CharField(max_length=140)),
                ('dianzanshu', models.IntegerField(default=0)),
                ('yonghu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jianyue.yonghu')),
            ],
        ),
    ]
