import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from main.models import Brand, CarModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Row, Column

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_tag = False
        self.helper.layout = (
            Row(
                Column('make'),
                Column('model'), 
                Column('year_from'), 
                Column('year_to'),
                css_class=''
            )
        )
    YEAR_CHOICES = [('',_('Select year'))] + [(r,r) for r in range(1990, datetime.date.today().year+1)]
    make = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label=_('Select make'), label='',
                                  widget=forms.Select(attrs={
                                      'name': 'make', 
                                      'hx-get': "models", # url
                                      'hx-trigger': 'change', # onchange
                                      'hx-target': '#id_model' # load model options
                                      })
                                )
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), empty_label=_('Select model'), label='',)
    year_from = forms.ChoiceField(choices=YEAR_CHOICES, initial=0, label='')
    year_to = forms.ChoiceField(choices=YEAR_CHOICES, initial=0, label='')
    
