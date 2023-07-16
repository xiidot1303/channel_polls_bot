from django.forms import ModelForm
from app.models import *
from django import forms

class TestForm(ModelForm):
    class Meta:
        model = Language
        fields = ['lang']
        widgets = {
            'lang': forms.TextInput(attrs={"class": "form-control"}),  
            
        }
    field_order = ['lang']