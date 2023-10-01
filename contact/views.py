from django.shortcuts import render,redirect
from django.contrib import messages 
from contact.forms import contactForm
from django.core.mail import send_mail


# Create your views here.
def contact(request):    
    submitted = False
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient = ['serkimdev@gmail.com']
            send_mail(subject, f'{message} from {sender}', sender, recipient, fail_silently=False)
            messages.success(request, 'Your message has sent.')
            return redirect('/contact?submitted=True')
    else:
        form = contactForm()
        if 'submitted' in request.GET:
            submitted = True
    
    context = {
        'submitted': submitted,
        'form': form
    }
    return render(request, 'contact/contact.html', context)