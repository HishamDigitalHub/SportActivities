# Generated by Django 2.1.1 on 2018-10-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamApp', '0014_auto_20181021_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='public_ind',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='teamimage',
            name='cover_img_ind',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='teamimage',
            name='profile_img_ind',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='teamimage',
            name='public_ind',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='teamvideo',
            name='public_ind',
            field=models.BooleanField(default=True),
        ),
    ]
