from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Drawing, BuildingName, DrawingFile, Project, MemberOfProject, DrawingUser
import re


class BuildingNameForm(ModelForm):
    class Meta:
        model = BuildingName
        fields=['name','abbreviation']

    def clean_abbreviation(self):
        abbreviation = self.cleaned_data['abbreviation']
        if not re.match(r'^[A-Z0-9]{1,3}$',abbreviation):
            raise ValidationError('The abbreviation can only contain uppercase letters or numbers')
        return abbreviation


class MembersOfProjectForm(ModelForm):
    email = forms.EmailField(help_text="A valid email address, please", required=True)

    class Meta:
        model = MemberOfProject
        fields=['status_user_perms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status_user_perms'].label = 'Project user status'

    def clean_status_user_perms(self):
        status_user_perms = self.cleaned_data['status_user_perms']
        if not re.match(r'^[A-Z0-9]{1,3}$',status_user_perms):
            raise ValidationError('The status_user_perms can only contain uppercase letters or numbers')

        return status_user_perms

    def clean_email(self):
        try:
            user = get_user_model().objects.get(email=self.cleaned_data['email'])
        except get_user_model().DoesNotExist:
            raise ValidationError('The user with the given email does not exist')
        if user.status !=self.cleaned_data['status_user_perms']:
            raise ValidationError('Status in project does not match user status')
        return self.cleaned_data['email']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields=['name','abbreviation']

    def clean_abbreviation(self):
        abbreviation = self.cleaned_data['abbreviation']
        if not re.match(r'^[A-Z0-9]{1,3}$',abbreviation):
            raise ValidationError('The abbreviation can only contain uppercase letters or numbers')
        return abbreviation


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
        required=False,
    )
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)


    class Meta:
        model = Drawing
        fields = ('draw_number','design_stage','branch',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['draw_number'].required = False
        self.fields['design_stage'].required = False
        self.fields['branch'].required = False
        self.fields['building_name'].queryset = BuildingName.objects.filter(project=args[1]).order_by('name')


class DrawingUserForm(forms.ModelForm):

    class Meta:
        model = DrawingUser
        fields = ('comment','status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label= 'Drawing status:'
        self.fields['comment'].label = 'Add comment:'



