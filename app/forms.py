from django import forms


class LinkForm(forms.Form):
    link = forms.CharField(help_text='Enter the link',widget=forms.DateInput(attrs={'type': 'text'}))
    tour = forms.ChoiceField(help_text="Choose a tour",widget=forms.DateInput(attrs={'type': 'text'}))
    start_date = forms.DateField(help_text='Enter start_date',widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(help_text='Enter end_date',widget=forms.DateInput(attrs={'type': 'date'}))
    child = forms.IntegerField(help_text='Enter child number',widget=forms.DateInput(attrs={'type': 'number'}))
    adult = forms.IntegerField(help_text='Enter adult number',widget=forms.DateInput(attrs={'type': 'number'}))
    nights_start = forms.IntegerField(help_text='Enter nights_start',widget=forms.DateInput(attrs={'type': 'number'}))
    nights_end = forms.IntegerField(help_text='Enter nights_end ',widget=forms.DateInput(attrs={'type': 'number'}))
    cost_min = forms.IntegerField(help_text='Minimum Price ',widget=forms.DateInput(attrs={'type': 'number'}))
    cost_max = forms.IntegerField(help_text='Maximum price ',widget=forms.DateInput(attrs={'type': 'number'}))
    
    