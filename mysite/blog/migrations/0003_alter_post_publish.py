# Generated by Django 5.0.7 on 2024-07-13 15:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_publish_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 13, 15, 1, 26, 81586, tzinfo=datetime.timezone.utc)),
        ),
    ]