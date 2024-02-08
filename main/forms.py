from django import forms
from .models import Post, PostImage, Brand, City
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
            Div(        
                Submit('submit', 'Place post', css_class='btn btn-primary btn-sm'),
                HTML('<a class="btn btn-secondary btn-sm" href="{% url \'home\' %}">Cancel</a>'),
                css_class="d-grid gap-2 d-md-block",
            )
        )

    class Meta:
        model = PostImage
        fields = ['images']
        labels = {
            'images': 'Add images of your car',
        }
        widgets = {
            'images': forms.ClearableFileInput(attrs={
                'multiple': True, 'class': 'form-control mb-2', 'label': 'add photos', 'required':'required'
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

    make = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label='Select car make')
    fuel_type = forms.ChoiceField(choices=FUEL_TYPE_CHOICES)
    # For 'model' field I am using 'smart-selects library'
    # 'empty_label' have been changed inside package (smart_selects)
    # /Users/kim/desktop/projects/.venvs/carsbay/lib/python3.10/site-packages/smart_selects/widgets.py
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
    

class PostUpdateForm(PostForm):
    # FUEL_TYPE_CHOICES = [('gas', 'Gasoline'), ('diesel', 'Diesel'), ('lpg', 'LPG/LPI'), ('electro', 'EV')]
    # fuel_type = forms.ChoiceField(widget=forms.RadioSelect, choices=FUEL_TYPE_CHOICES)

    class Meta:
        model = Post
        fields = ['make', 'model','city','year', 'fuel_type', 'price', 'mileage', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
