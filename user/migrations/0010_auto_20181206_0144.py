# Generated by Django 2.1.1 on 2018-12-06 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_timelog_text2break'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='writter_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='grade',
            field=models.CharField(max_length=10),
        ),
    ]
