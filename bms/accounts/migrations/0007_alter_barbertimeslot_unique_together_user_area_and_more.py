# Generated by Django 5.0.4 on 2024-04-23 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_barbertimeslot_timeslot'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='barbertimeslot',
            unique_together={('user', 'day_of_week')},
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.RemoveField(
            model_name='barbertimeslot',
            name='available_end',
        ),
        migrations.RemoveField(
            model_name='barbertimeslot',
            name='available_start',
        ),
    ]
