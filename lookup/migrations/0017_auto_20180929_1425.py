# Generated by Django 2.1.1 on 2018-09-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0016_auto_20180927_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='icon',
            field=models.ImageField(upload_to='country/images/'),
        ),
    ]
