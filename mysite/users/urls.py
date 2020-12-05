from django.contrib import admin
from django.urls import path, include
from users import views
from users.views import (
	UserRegisterView,
	UserUpdateView,
	PasswordsChangeView,
	ShowProfilePageView,
)



urlpatterns = [
	path('register/', UserRegisterView.as_view(), name='register'),
    path('edit-profile/', UserUpdateView.as_view(),name='edit-profile'),
    path('password-success/', views.password_success,name='password-success'),
    path('password/',PasswordsChangeView.as_view(template_name='users/change_password.html')),
    path('show-profile/<int:pk>/', ShowProfilePageView.as_view(),name='show-profile'),
    ]