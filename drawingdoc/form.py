from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Drawing, BuildingName, DrawingFile, Project


class DrawingForm(ModelForm):
    class Meta:
        model = Drawing
        fields= ['design_stage','branch','date_drawing','date_update','draw_number', 'draw_title', 'building_name', 'revision']


class BuildingNameForm(ModelForm):
    class Meta:
        model = BuildingName
        fields=['name','abbreviation',]


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields=['name','abbreviation',]


class UploadDrawingForm(ModelForm):
    class Meta:
        model = DrawingFile
        fields=['file_field',]
        widgets = {
            'file_field' : forms.ClearableFileInput(attrs={'multiple': True})
        }


class DrawingsSearchForm(forms.ModelForm):

    building_name = forms.ModelMultipleChoiceField(
        queryset=BuildingName.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)


    class Meta:
        model = Drawing
        fields = ('draw_number','design_stage','branch',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['draw_number'].required = False
