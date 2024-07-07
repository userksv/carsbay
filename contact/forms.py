from django import forms
from django.utils.translation import gettext_lazy as _


class contactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': _('Subject')}))
    sender = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': _('Your email')}))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': _('Write your message...')}))