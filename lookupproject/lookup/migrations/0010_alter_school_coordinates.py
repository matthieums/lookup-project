# Generated by Django 5.1.3 on 2025-02-16 19:06

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0009_alter_course_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0, srid=4326), srid=4326),
        ),
    ]
