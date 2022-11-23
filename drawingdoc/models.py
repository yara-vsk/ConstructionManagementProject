from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class BuildingName(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Drawing(models.Model):

    class DesignStage(models.TextChoices):
        ds1 = 'PK', _('PROJEKT KONCEPCYJNY')
        ds2 = 'PB', _('PROJEKT BUDOWLANY')
        ds3 = 'PW.', _('PROJEKT WYKONAWCZY')

    class Branch(models.TextChoices):
        b1 = 'A', _('Architektura')
        b2 = 'K', _('Konstrukcja')
        b3 = 'E', _('Instalacje elektryczne')
        b4 = 'IS', _('Instalacje sanitarne')
        b5 = 'D', _('Drogi')

    design_stage = models.CharField(max_length=3,choices=DesignStage.choices, default=DesignStage.ds3)
    branch = models.CharField(max_length=3,choices=Branch.choices, default=Branch.b1)
    date_drawing = models.DateField()
    date_update = models.DateField()
    draw_number = models.CharField(max_length=10)
    draw_title = models.CharField(max_length=200)
    building_name = models.ForeignKey(BuildingName, on_delete=models.CASCADE)
    revision = models.CharField(max_length=3)

    def __str__(self):
        return self.id
