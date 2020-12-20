from django import forms

from .models import TestModel


class TestModelForm(forms.ModelForm):

    class Meta:
        model = TestModel
        fields = '__all__'


class TestForm(forms.Form):
    title = forms.CharField(max_length=255)
