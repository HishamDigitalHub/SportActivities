# Generated by Django 2.1.1 on 2018-09-25 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistrationApp', '0034_profile_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='google_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='longitude',
            field=models.FloatField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
