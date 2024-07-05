from django.urls import path
from .import views
from .views import PostDetailView, PostUpdateView, PostDeleteView, PostView, PostCreateView
from django.conf.urls.static import static
from django.conf import settings
from main.api import services

urlpatterns = [
    path('', PostView.as_view(), name='home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='about'),
    path('post-images/<int:pk>/', services.fetch_post_images, name='post-images'),
    path('post/new/models/', views.models, name='models'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)