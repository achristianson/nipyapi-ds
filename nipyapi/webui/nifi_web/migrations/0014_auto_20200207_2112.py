# Generated by Django 2.2.7 on 2020-02-07 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0013_instancetype_instancetypeenvvar_instancetypeport'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMirror',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auth', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='nifi_web.DockerRegistryAuth')),
            ],
        ),
        migrations.RemoveField(
            model_name='instancetype',
            name='auth',
        ),
        migrations.CreateModel(
            name='ImageMirrorJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(default='PENDING_MIRROR', max_length=100)),
                ('docker_id', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mirror', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nifi_web.ImageMirror')),
            ],
        ),
    ]
