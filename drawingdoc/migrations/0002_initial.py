# Generated by Django 4.1.3 on 2023-03-04 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawingdoc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberofproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.project'),
        ),
        migrations.AddField(
            model_name='memberofproject',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drawinguser',
            name='drawing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.drawing'),
        ),
        migrations.AddField(
            model_name='drawinguser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drawing',
            name='building_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.buildingname'),
        ),
        migrations.AddField(
            model_name='drawing',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.drawingfile'),
        ),
        migrations.AddField(
            model_name='drawing',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.project'),
        ),
        migrations.AddField(
            model_name='buildingname',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawingdoc.project'),
        ),
    ]
