# Generated by Django 2.2.7 on 2019-12-09 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0007_nifiimage_mvn_build_args'),
    ]

    operations = [
        migrations.AddField(
            model_name='nifiinstance',
            name='namespace',
            field=models.CharField(default='default', max_length=100),
            preserve_default=False,
        ),
    ]
