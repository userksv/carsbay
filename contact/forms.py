from django import forms


class contactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    sender = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Write your message...'}))