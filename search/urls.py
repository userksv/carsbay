from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchResultView.as_view(), name='search'),
    # path('search-resutl/', views.search_result, name='search-result')
]