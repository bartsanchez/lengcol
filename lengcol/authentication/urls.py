from django.contrib.auth import views as auth_views
from django.urls import path

from authentication import views

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='authentication/login.html',
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='authentication/logout.html',
        ),
        name='logout'
    ),
    path('register/', views.RegisterView.as_view(), name='register'),
]
