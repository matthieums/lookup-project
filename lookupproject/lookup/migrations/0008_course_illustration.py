# Generated by Django 5.1.3 on 2025-01-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup', '0007_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='illustration',
            field=models.ImageField(blank=True, default='default/default_image.jpg', upload_to='images/'),
        ),
    ]
