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
            'images': 'Add images of your car',
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
        
    FUEL_TYPE_CHOICES = [('','Select fuel type')] + [('gas', 'Gasoline'), ('diesel', 'Diesel'), ('lpg', 'LPG/LPI'), ('electro', 'EV')]
    YEAR_CHOICES = [('','Select year')] + [(r,r) for r in range(1990, datetime.date.today().year+1)]

    make = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label='Select car make',
                                   widget=forms.Select(attrs={
                                      'name': 'make', 
                                      'hx-get': "models", # url
                                      'hx-trigger': 'change', # onchange
                                      'hx-target': '#id_model' # load model options
                                      }))
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), empty_label='Select model')
    fuel_type = forms.ChoiceField(choices=FUEL_TYPE_CHOICES)
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label='Select city')
    year = forms.ChoiceField(choices=YEAR_CHOICES,initial=0)
    mileage = forms.DecimalField(widget=forms.NumberInput(attrs={'type':'number', 'placeholder': 0}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'type':'number', 'placeholder': 0}))
    description = forms.TextInput()
                               
    class Meta:
        model = Post
        fields = ['make', 'model','city','year', 'fuel_type', 'price', 'mileage', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':15, 'placeholder': 'Write a short description'}),
        }
    

class PostUpdateForm(PostForm, PostImageForm):
    class Meta:
        model = Post
        fields = ['make', 'model','city','year', 'fuel_type', 'price', 'mileage', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
