import datetime
from django import forms
from main.models import Brand, CarModel

class SearchForm(forms.Form):
    YEAR_CHOICES = [('','Select year')] + [(r,r) for r in range(1990, datetime.date.today().year+1)]
    
    make = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label='Select car make',
                                  widget=forms.Select(attrs={
                                      'name': 'make', 
                                      'hx-get': "models", # url
                                      'hx-trigger': 'change', # onchange
                                      'hx-target': '#id_model' # load model options
                                      })
                                )
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), empty_label='Select model')
    year_from = forms.ChoiceField(choices=YEAR_CHOICES, initial=0, label='from')
    year_to = forms.ChoiceField(choices=YEAR_CHOICES, initial=0, label='to')
