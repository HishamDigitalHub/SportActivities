# Generated by Django 2.1.1 on 2018-09-27 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0015_auto_20180927_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='icon',
            field=models.ImageField(upload_to='country/'),
        ),
    ]
