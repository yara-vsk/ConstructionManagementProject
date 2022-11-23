# Generated by Django 4.1.3 on 2022-11-23 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('abbreviation', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design_stage', models.CharField(choices=[('PK', 'PROJEKT KONCEPCYJNY'), ('PB', 'PROJEKT BUDOWLANY'), ('PW.', 'PROJEKT WYKONAWCZY')], default='PW.', max_length=3)),
                ('branch', models.CharField(choices=[('A', 'Architektura'), ('K', 'Konstrukcja'), ('E', 'Instalacje elektryczne'), ('IS', 'Instalacje sanitarne'), ('D', 'Drogi')], default='A', max_length=3)),
                ('date_drawing', models.DateField()),
                ('date_update', models.DateField()),
                ('draw_number', models.CharField(max_length=10)),
                ('draw_title', models.CharField(max_length=200)),
                ('building_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.buildingname')),
            ],
        ),
    ]
