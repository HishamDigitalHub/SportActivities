# Generated by Django 2.1.1 on 2018-10-24 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistrationApp', '0049_auto_20181024_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='user',
        ),
    ]
