# Generated by Django 2.1.1 on 2018-12-15 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_auto_20181216_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterequest',
            name='origin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='originRequestInfo', to='user.EnterTimelog'),
            preserve_default=False,
        ),
    ]