# Generated by Django 2.1.1 on 2018-09-24 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistrationApp', '0032_profile_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='test',
        ),
    ]
