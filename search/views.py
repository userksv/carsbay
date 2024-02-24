
from django.views.generic import FormView
from django.urls import reverse
from .forms import SearchForm


class SearchResultView(FormView):
    form_class = SearchForm
    template_name = 'search/search.html'

    def form_valid(self, form):
        make = form.cleaned_data['make']
        year_from = form.cleaned_data['year_from']
        year_to = form.cleaned_data['year_to']
        
        print(make, year_from, year_to)
        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
       return reverse('search')