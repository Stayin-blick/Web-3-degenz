# Generated by Django 3.2.20 on 2023-10-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_auto_20230830_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='last_visited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]