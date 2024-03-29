from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from .drawingsnamechecker import drawings_name_checker


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MemberOfProject(models.Model):

    class Status(models.TextChoices):
        s1 = 'AR', _('Architekt')
        s2 = 'INW', _('Inwestor')
        s3 = 'GW', _('Generalny Wykonawca')
        s4 = 'INI', _('Inspektor Nadzoru')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status_user_perms = models.CharField(max_length=100, choices=Status.choices, default=Status.s1)


class BuildingName(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def directory_path(instance, filename):
    drawing_data = drawings_name_checker(filename)
    return 'uploads/{project}/{stage}/{branch}/{building_name}/{name}'.format(project=drawing_data['project'],
                                                                              stage=drawing_data['design_stage'],
                                                                              branch=drawing_data['branch'],
                                                                              building_name=drawing_data[
                                                                                  'building_name'],
                                                                              name=filename)


class DrawingFile(models.Model):
    file_field = models.FileField(upload_to=directory_path)
    file_name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.file_name


class Drawing(models.Model):
    class DesignStage(models.TextChoices):
        ds1 = 'PW', _('Projekt wykonawczy')
        ds2 = 'PB', _('Projekt budowlany')
        ds3 = 'PK', _('Projekt koncepcyjny')

    class Branch(models.TextChoices):
        b1 = 'A', _('Architektura')
        b2 = 'K', _('Konstrukcja')
        b3 = 'E', _('Instalacje elektryczne')
        b4 = 'IS', _('Instalacje sanitarne')
        b5 = 'D', _('Drogi')

    design_stage = models.CharField(max_length=3, choices=DesignStage.choices, default=DesignStage.ds1)
    branch = models.CharField(max_length=3, choices=Branch.choices, default=Branch.b1)
    date_drawing = models.DateField()
    date_update = models.DateField()
    draw_number = models.CharField(max_length=10)
    draw_title = models.CharField(max_length=200)
    building_name = models.ForeignKey(BuildingName, on_delete=models.CASCADE)
    revision = models.CharField(max_length=3)
    file = models.ForeignKey(DrawingFile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.file


class DrawingUser(models.Model):

    class Status(models.TextChoices):
        s1 = 'accepted', _('accepted')
        s2 = 'to correct', _('to correct')
        s3 = 'uploaded', _('uploaded')
        __empty__ = _(' ')

    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.TextField(max_length=1400, blank=True)
    status = models.CharField(max_length=100, choices=Status.choices, blank=True)
