from django import forms
from django.contrib.auth import get_user_model

from .models import TestModel


User = get_user_model()


class TestModelForm(forms.ModelForm):

    class Meta:
        model = TestModel
        fields = '__all__'


class TestForm(forms.Form):
    title = forms.CharField(max_length=255)
