# Generated by Django 2.1.1 on 2018-12-06 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20181206_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='grade',
            field=models.IntegerField(),
        ),
    ]
