from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Row, Column, Fieldset
from crispy_forms.bootstrap import InlineRadios

from django.contrib.auth.forms import PasswordResetForm
class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("There is no user registered with the specified E-Mail address.")
            self.add_error('email', msg)
        return email
    

class UserRegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'password1']
    
    # This is for reference
    # fields = ['username', 'email', 'password1']
    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'username'})
    #     self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'email'})
    #     self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'password'})
    #     self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'repeat password'})
        

""" Update user profile fields """
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


""" Update user profile image """
class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'phone_number'
        )

    class Meta:
        model = Profile
        fields = ['image', 'phone_number']


class ExampleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first arg is the legend of the fieldset',
                'favorite_number',
                'favorite_color',
                'favorite_food',
                HTML("""<p>We use notes to get better, <strong>please help us {{ username }}</strong></p>"""),
                'notes',
            Row(
                Column('name'),
                Column('email'),
                Column(InlineRadios('like_website')),
                ),
            Submit('submit', 'Submit', css_class='button white'),
        )

    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )

    name = forms.CharField(
        label = 'What is your name?',
        required=False
    )

    email = forms.EmailField(
        label='What is your email?',
        required=False
    )

