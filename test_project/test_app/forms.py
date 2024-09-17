# forms.py
from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


class CompanyFilterForm(forms.Form):
    name = forms.CharField(required=False, max_length=255)
    industry = forms.CharField(required=False, max_length=255)
    country = forms.CharField(required=False, max_length=255)
    min_revenue = forms.DecimalField(required=False, min_value=0)
    max_revenue = forms.DecimalField(required=False, min_value=0)
