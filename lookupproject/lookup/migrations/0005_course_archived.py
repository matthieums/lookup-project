# Generated by Django 5.1.3 on 2025-01-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0004_course_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
