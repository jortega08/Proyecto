# Generated by Django 5.1.2 on 2024-11-10 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensores', '0002_batterystatus_currentdata_delete_sensordata_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='batterystatus',
            name='sensores_ba_timesta_77fccb_idx',
        ),
        migrations.RemoveIndex(
            model_name='currentdata',
            name='sensores_cu_timesta_c3ee26_idx',
        ),
    ]