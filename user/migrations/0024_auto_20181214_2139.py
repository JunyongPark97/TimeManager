# Generated by Django 2.1.1 on 2018-12-14 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_auto_20181214_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='writter_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
