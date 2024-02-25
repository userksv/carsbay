from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchForm.as_view(), name='search'),
    path('search-result/', views.SearchResultView.as_view(), name='search-result'),
    path('models/', views.models, name='models'),
]
