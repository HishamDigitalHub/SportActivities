# Generated by Django 2.1.1 on 2018-09-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistrationApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.CharField(max_length=15)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('DOB', models.DateField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('facebook_id', models.TextField()),
                ('google_id', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userextension',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserExtension',
        ),
    ]
