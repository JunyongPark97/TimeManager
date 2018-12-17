# Generated by Django 2.1.1 on 2018-12-17 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_entertimelog_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterathometimelog',
            name='keyword',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
        migrations.AddField(
            model_name='outathometimelog',
            name='keyword',
            field=models.IntegerField(blank=True, default=4, null=True),
        ),
        migrations.AddField(
            model_name='outtimelog',
            name='keyword',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
    ]