# Generated by Django 2.2.7 on 2019-12-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0010_nifiinstance_deploy_jupyter'),
    ]

    operations = [
        migrations.AddField(
            model_name='nifiinstance',
            name='jupyter_token',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
