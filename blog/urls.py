from django.urls import path

from blog import views

urlpatterns = [
    path('', views.BlogPostView.as_view(), name='blog')
]