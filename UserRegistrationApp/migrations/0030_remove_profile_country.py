# Generated by Django 2.1.1 on 2018-09-24 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistrationApp', '0029_auto_20180924_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
    ]
