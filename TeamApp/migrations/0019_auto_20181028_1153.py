# Generated by Django 2.1.1 on 2018-10-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0018_sport_sporticon'),
        ('TeamApp', '0018_auto_20181025_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teampreference',
            name='sport',
        ),
        migrations.AddField(
            model_name='teampreference',
            name='sport',
            field=models.ManyToManyField(blank=True, to='lookup.Sport'),
        ),
    ]
