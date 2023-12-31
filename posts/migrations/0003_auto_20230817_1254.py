# Generated by Django 3.2.20 on 2023-08-17 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
        ('posts', '0002_post_image_filter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_filter',
        ),
        migrations.AddField(
            model_name='post',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='communities.community'),
        ),
    ]
