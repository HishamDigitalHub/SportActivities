# Generated by Django 2.1.1 on 2018-11-01 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0018_sport_sporticon'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('VenueApp', '0006_auto_20181021_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')], max_length=1, null=True)),
                ('min_age', models.IntegerField(blank=True, null=True)),
                ('max_age', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='venue_preference_created_by', to=settings.AUTH_USER_MODEL)),
                ('sport', models.ManyToManyField(blank=True, related_name='activity_preference_sport', to='lookup.Sport')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='venue_preference_updated_by', to=settings.AUTH_USER_MODEL)),
                ('venue', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venue_activity', to='VenueApp.Venue')),
            ],
        ),
    ]
