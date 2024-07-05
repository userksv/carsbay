import json
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from main.models import Post, PostImage, get_models
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from main.forms import PostForm, PostUpdateForm, PostImageForm
from django.urls import reverse


class PostView(ListView):
    paginate_by = 8
    model = Post
    template_name = "main/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'main/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form2"] = PostImageForm()
        return context

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.author = self.request.user
        self.instance.save()

        ####### This form does not work with small images!!!!!!
        form2 = PostImageForm(self.request.POST, self.request.FILES)
        if form2.is_valid():
            print("Form2 valid")
            images = self.request.FILES.getlist("images")
            for image in images:
                PostImage.objects.create(post=self.instance, images=image)

        messages.success(self.request, "Your post has been created!")
        return redirect(self.get_success_url())

    def get_success_url(self):
        # pk = self.instance.id
        return reverse("post-detail", kwargs={"pk": self.instance.id})


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    # Add "delete images functionality"
    model = Post
    form_class = PostUpdateForm
    template_name = "main/post_update.html"
    
    images_to_update = []

    def get_success_url(self):
        return reverse("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form2"] = PostImageForm(self.request.FILES)
        images = PostImage.objects.filter(post=self.get_object())
        context['images'] = [{'url': image.images.url, 'id': image.id} for image in images]
        return context
    
    def put(self, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.method == 'PUT':
            # Get post image instance by id from request and 
            # construct list of objects for further deletion on form_valid
            image_id = json.loads(self.request.body.decode('utf-8'))['imageId']
            print(image_id)
            if image_id is None:
                return HttpResponse( 'Image not found', status=404)
            image_instance = PostImage.objects.get(id=image_id)
            self.images_to_update.append(image_instance)
        return HttpResponse('Ok', status=200)
    
    """ Checks user authorization """
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def form_valid(self, form):
        form2 = PostImageForm(self.request.POST, self.request.FILES)

        if self.images_to_update:
            for image in self.images_to_update:
                print(image)
                try:
                    image.delete()
                except:
                    print('File not found')
            self.images_to_update = []
        
        if form2.is_valid():
            images = self.request.FILES.getlist("images")
            for image in images:
                PostImage.objects.create(post=self.object, images=image)
                ...

        messages.success(self.request, f"Your post has been updated!")
        return super().form_valid(form)


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = "main/post_del_confirm.html"

    # success_url = 'profile/'
    def get_success_url(self):
        post = self.get_object()
        return reverse("profile")

    def form_valid(self, form):
        messages.success(self.request, f"Your post has been deleted sucessfully!")
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, "main/about.html", {"title": "About"})

def models(request):
    make = request.GET.get('make')
    
    models = get_models(make)
    context = {
        'models': models
    }
    return render(request, 'main/models.html', context)
