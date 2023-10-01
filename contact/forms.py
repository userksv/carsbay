from django import forms


class contactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Subject')
    sender = forms.EmailField(label='Your email')
    message = forms.CharField(widget=forms.Textarea)