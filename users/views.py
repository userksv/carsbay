from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ExampleForm
from django.contrib.auth import user_logged_in
from main.models import Post, PostImage
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from .api.serializers import ProfileSerializer
from django.http import JsonResponse


# Create your views here.
def logged_in_message(sender, user, request, **kwargs):
    """
    Add a welcome message when the user logs in
    """
    messages.info(request, f'Welcome {user.username}!')

user_logged_in.connect(logged_in_message)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # get data from register form and clean it
        if form.is_valid():
            form.save()#
            messages.success(request, f'Your account has been created! Now you can log in')
            return redirect('login')
    else :
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile(request):
    author_id = request.user.id
    posts = Post.objects.filter(author=author_id)
    context = {
        'posts': posts,
        'title': 'Profile page',
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    e_form = ExampleForm()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if 'cancel' in request.POST:
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()#
            p_form.save()#
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'e_form': e_form,
        'title': 'Profile page',
    }
    return render(request, 'users/profile-update.html', context)

@login_required
def my_posts(request):
    author_id = request.user.id
    posts = Post.objects.filter(author=author_id)
    context = {
        'posts': posts,
        'title': 'Profile page',
    }
    return render(request, 'users/my-posts.html', context)

@csrf_exempt
def get_user_profile_image(request, id):
    profile = Profile.objects.get(user=id)
    serializer = ProfileSerializer(profile).data
    return JsonResponse(serializer, safe=False)

def delete_profile_image(request, id):
    print("Delete profile image")
    print(request)
    return