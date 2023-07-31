from django import forms


class LinkForm(forms.Form):
    link = forms.CharField(help_text='Enter the link', )
