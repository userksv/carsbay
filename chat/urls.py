from django.urls import path
from .import views


urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('room1', views.room1, name='room1'),
    # path('chat/', views.chat_view, name='chat'),
]