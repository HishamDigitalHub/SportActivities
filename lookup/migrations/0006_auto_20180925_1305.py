# Generated by Django 2.1.1 on 2018-09-25 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0005_auto_20180924_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_id', to='lookup.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'country')},
        ),
    ]
