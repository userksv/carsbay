from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Post, PostImage, Brand, City, CarModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Row, Column
import datetime


class PostImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'images',
        )

    class Meta:
        model = PostImage
        fields = ['images']
        labels = {
            'images': _('Add images of your car'),
        }
        widgets = {
            'images': forms.ClearableFileInput(attrs={
                'multiple': True, 'class': 'form-control mb-2', 'label': 'add photos'
                }
            ),
        }


class PostForm(PostImageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-group'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('make'),
                Column('model'),
            ),
            Row(
                Column('year'),
                Column('city'),
            ),
            Row(
                Column('fuel_type'),
                Column('mileage'),
                Column('price'),
            ),
            'description',
        )
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = CarModel.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['model'].queryset = self.instance.make.models.order_by('name')
        else:
            self.fields['model'].queryset = CarModel.objects.none()
        
    FUEL_TYPE_CHOICES = [('',_('Select fuel type'))] + [('gas', 'Gasoline'), ('diesel', 'Diesel'), ('lpg', 'LPG/LPI'), ('electro', 'EV')]
    YEAR_CHOICES = [('',_('Select year'))] + [(r,r) for r in range(1990, datetime.date.today().year+1)]

    make = forms.ModelChoiceField(label=_('make'), queryset=Brand.objects.all(), empty_label=_('Select car make'),
                                   widget=forms.Select(attrs={
                                      'name': 'make', 
                                      'hx-get': "models", # url
                                      'hx-trigger': 'change', # onchange
                                      'hx-target': '#id_model' # load model options
                                      }))
    model = forms.ModelChoiceField(label=_('model'), queryset=CarModel.objects.none(), empty_label=_('Select model'))
    fuel_type = forms.ChoiceField(label=_('fuel type'), choices=FUEL_TYPE_CHOICES)
    city = forms.ModelChoiceField(label=_('city'), queryset=City.objects.all(), empty_label=_('Select city'))
    year = forms.ChoiceField(label=_('year'), choices=YEAR_CHOICES,initial=0)
    mileage = forms.DecimalField(label=_('mileage'), widget=forms.NumberInput(attrs={'type':'number', 'placeholder': 0}))
    price = forms.DecimalField(label=_('price'), widget=forms.NumberInput(attrs={'type':'number', 'placeholder': 0}))
    description = forms.TextInput(attrs={'type': 'label'})
                               
    class Meta:
        model = Post
        fields = ['make', 'model','city','year', 'fuel_type', 'price', 'mileage', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':15, 'placeholder': _('Write a short description')}),
        }
    

class PostUpdateForm(PostForm, PostImageForm):
    class Meta:
        model = Post
        fields = ['make', 'model', 'city', 'year', 'fuel_type', 'price', 'mileage', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
