from django import forms
from .models import BookCall, HireMe


class BookCallForm(forms.ModelForm):
    class Meta:
        model = BookCall
        fields = ['name', 'email', 'phone', 'preferred_date', 'preferred_time']


class HireMeForm(forms.ModelForm):
    class Meta:
        model = HireMe
        fields = ['name', 'email', 'project_details']
