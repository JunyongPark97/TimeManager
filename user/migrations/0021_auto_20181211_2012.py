# Generated by Django 2.1.1 on 2018-12-11 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('user', '0020_requestinfo_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterAtHomeTimelog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('text', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnterTimelog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('text', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutAtHomeTimelog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('text', models.CharField(max_length=10)),
                ('breaktime', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutTimelog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('text', models.CharField(max_length=10)),
                ('half_day_off', models.CharField(blank=True, max_length=10, null=True)),
                ('breaktime', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('update', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, '대기중'), (1, '수락'), (2, '거절')], default=0)),
                ('reason', models.TextField(null=True)),
                ('breaktime', models.IntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiverRequestinfo', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senderRequestinfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='timelog',
        ),
        migrations.RemoveField(
            model_name='timeinfo',
            name='timelog',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='user',
        ),
        migrations.DeleteModel(
            name='RequestInfo',
        ),
        migrations.DeleteModel(
            name='Timeinfo',
        ),
        migrations.DeleteModel(
            name='Timelog',
        ),
    ]
