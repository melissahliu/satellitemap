# Generated by Django 3.2.20 on 2023-08-31 22:17

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('satmap', '0002_auto_20230831_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='location',
            field=location_field.models.plain.PlainLocationField(max_length=63),
        ),
    ]