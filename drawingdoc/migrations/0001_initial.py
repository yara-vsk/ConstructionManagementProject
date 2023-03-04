# Generated by Django 4.1.3 on 2023-03-04 15:30

from django.db import migrations, models
import drawingdoc.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abbreviation', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design_stage', models.CharField(choices=[('PW', 'Projekt wykonawczy'), ('PB', 'Projekt budowlany'), ('PK', 'Projekt koncepcyjny')], default='PW', max_length=3)),
                ('branch', models.CharField(choices=[('A', 'Architektura'), ('K', 'Konstrukcja'), ('E', 'Instalacje elektryczne'), ('IS', 'Instalacje sanitarne'), ('D', 'Drogi')], default='A', max_length=3)),
                ('date_drawing', models.DateField()),
                ('date_update', models.DateField()),
                ('draw_number', models.CharField(max_length=10)),
                ('draw_title', models.CharField(max_length=200)),
                ('revision', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='DrawingFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_field', models.FileField(upload_to=drawingdoc.models.directory_path)),
                ('file_name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DrawingUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('comment', models.TextField(blank=True, max_length=1400)),
                ('status', models.CharField(blank=True, choices=[(None, ' '), ('accepted', 'accepted'), ('to correct', 'to correct'), ('uploaded', 'uploaded')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MemberOfProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_user_perms', models.CharField(choices=[('AR', 'Architekt'), ('INW', 'Inwestor'), ('GW', 'Generalny Wykonawca'), ('INI', 'Inspektor Nadzoru')], default='AR', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abbreviation', models.CharField(max_length=3, unique=True)),
            ],
        ),
    ]
