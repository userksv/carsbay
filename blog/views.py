from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class BlogPostView(TemplateView):
    template_name = 'blog/blog.html'