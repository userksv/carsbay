from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import PostImage

# this view only for testing
def room1(request):
    return render(request, 'chat/chat1.html')

def room2(request):
    return render(request, 'chat/chat2.html')

@login_required
def chat_view(request):
    return render(request, 'chat/chat.html')

