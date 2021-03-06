# Generated by Django 2.1.1 on 2018-10-24 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('UserRegistrationApp', '0046_profile_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='user',
        ),
        migrations.AddField(
            model_name='preference',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preference',
            name='request_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
    ]
