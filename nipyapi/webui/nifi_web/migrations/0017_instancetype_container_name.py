# Generated by Django 2.2.7 on 2020-02-11 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0016_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancetype',
            name='container_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]