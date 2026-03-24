from django import forms
from myapp.models import uv

class uvForm(forms.ModelForm):
    class Meta:
        model = uv
        fields = ['thereshold']


