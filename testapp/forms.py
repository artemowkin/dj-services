from django import forms


class TestForm(forms.Form):
    title = forms.CharField(max_length=255)
