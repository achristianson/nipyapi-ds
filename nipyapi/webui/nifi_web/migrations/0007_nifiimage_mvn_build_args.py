# Generated by Django 2.2.7 on 2019-11-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0006_auto_20191107_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='nifiimage',
            name='mvn_build_args',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
