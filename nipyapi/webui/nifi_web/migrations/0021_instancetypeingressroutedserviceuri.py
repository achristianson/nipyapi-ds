# Generated by Django 2.2.7 on 2020-02-27 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nifi_web', '0020_auto_20200213_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceTypeIngressRoutedServiceURI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('path', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instance_type_svc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nifi_web.InstanceTypeIngressRoutedService')),
            ],
        ),
    ]
