from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, FormView, TemplateView, CreateView
from django.db.models import Q
from main.models import get_models, Post
from .forms import SearchForm

class SearchForm(FormView, ListView):
    model = Post
    template_name = 'search/search.html'
    form_class = SearchForm

    def form_valid(self, form: Any) -> HttpResponse:
        print(form.data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("search-result/")


class SearchResultView(ListView):
    model = Post
    template_name = 'search/search_result.html'

    def post(self):
        return 
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        y_from = int(self.request.GET.get('year_from'))
        year_to = int(self.request.GET.get('year_to'))
        if y_from > year_to:
            return redirect('/search/')
        self.get_queryset()

        return super().get(request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        model = self.request.GET.get('model')
        y_from = int(self.request.GET.get('year_from'))
        year_to = int(self.request.GET.get('year_to'))
        object_list = Post.objects.filter(model=model, year__range=[y_from, year_to])
        
        return object_list

    
def models(request):
    make = request.GET.get('make')
    
    models = get_models(make)
    context = {
        'models': models
    }
    return render(request, 'search/models.html', context)
