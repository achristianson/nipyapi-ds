# Generated by Django 2.2.7 on 2020-02-06 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0012_dockerregistryauth'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auth', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='nifi_web.DockerRegistryAuth')),
            ],
        ),
        migrations.CreateModel(
            name='InstanceTypePort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal', models.IntegerField()),
                ('external', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nifi_web.InstanceType')),
            ],
        ),
        migrations.CreateModel(
            name='InstanceTypeEnvVar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('default_value', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nifi_web.InstanceType')),
            ],
        ),
    ]