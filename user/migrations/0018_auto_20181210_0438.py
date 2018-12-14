# Generated by Django 2.1.1 on 2018-12-10 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20181206_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelog',
            name='half_day_off',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='keyword',
            field=models.IntegerField(choices=[(1, '출근'), (2, '퇴근'), (3, '출근 (재택)'), (4, '퇴근 (재택)')]),
        ),
    ]
