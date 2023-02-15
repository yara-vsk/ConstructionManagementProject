import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms

from schedule.models import Schedule


class UploadScheduleForm(ModelForm):
    file_csv = forms.FileField()

    class Meta:
        model = Schedule
        fields = []

    def clean_file_csv(self):
        file_csv = self.cleaned_data['file_csv']
        if not re.match(r'.*csv$',file_csv.name):
            raise ValidationError('Please, upload ".csv" file')
        return file_csv

