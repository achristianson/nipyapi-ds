# Generated by Django 2.2.7 on 2020-02-07 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0015_auto_20200207_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instance_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nifi_web.InstanceType')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nifi_web.NifiInstance')),
            ],
        ),
    ]
