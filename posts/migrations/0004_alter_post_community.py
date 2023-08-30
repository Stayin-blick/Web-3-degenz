# Generated by Django 3.2.20 on 2023-08-30 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_auto_20230830_1657'),
        ('posts', '0003_auto_20230817_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='community',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='communities.community'),
        ),
    ]