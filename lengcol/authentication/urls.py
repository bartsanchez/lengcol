from django.urls import path

from authentication import views

urlpatterns = [
    path(
        "login/",
        views.CustomLoginView.as_view(
            template_name="authentication/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        views.CustomLogoutView.as_view(
            template_name="authentication/logout.html",
        ),
        name="logout",
    ),
    path("register/", views.RegisterView.as_view(), name="register"),
]
