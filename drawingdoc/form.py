from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Drawing, BuildingName


class DrawingForm(ModelForm):
    class Meta:
        model = Drawing
        fields= ['design_stage','branch','date_drawing','date_update','draw_number', 'draw_title', 'building_name', 'revision']

class BuildingNameForm(ModelForm):
    class Meta:
        model = BuildingName
        fields=['name','abbreviation',]