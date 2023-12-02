from django.urls import path
from django.contrib.auth import  views as auth_views
from users import views as users_views
from users.forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', users_views.register,name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', users_views.profile, name='profile'),
    path('profile-update/', users_views.profile_update, name='profile-update'),
    path('my-posts/', users_views.my_posts, name='my-posts'),
    path('get-image/<int:id>', users_views.get_user_profile_image, name='get-image'),
    path('delete-profile-image/<int:id>', users_views.get_user_profile_image, name='delete-profile-image'),

    # starting point for reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', form_class=EmailValidationOnForgotPassword), name='password-reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
