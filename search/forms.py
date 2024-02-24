import datetime
from django import forms
from main.models import Brand, CarModel, Post
from smart_selects.db_fields import ChainedForeignKey
from smart_selects.form_fields import ChainedModelChoiceField
from smart_selects.db_fields import ChainedForeignKey

class SearchForm(forms.Form):
    YEAR_CHOICES = [('','Select year')] + [(r,r) for r in range(1990, datetime.date.today().year+1)]
    
    make = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label='Select car make')
  
    year_from = forms.ChoiceField(choices=YEAR_CHOICES, initial=0, label='from')
    year_to = forms.ChoiceField(choices=YEAR_CHOICES, initial=0, label='to')
