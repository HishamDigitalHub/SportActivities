# Generated by Django 2.1.1 on 2018-09-20 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistrationApp', '0004_userextension_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextension',
            name='user',
        ),
    ]
