# Generated by Django 2.1.1 on 2018-09-24 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0003_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('country', models.ManyToManyField(to='lookup.Country')),
            ],
        ),
    ]
