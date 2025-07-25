# Generated by Django 4.0.6 on 2024-11-01 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archive_app', '0001_initial'),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='archiviste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.archivist'),
        ),
        migrations.AddField(
            model_name='archive',
            name='patrimoine',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='archive_app.patrimoine'),
        ),
    ]
