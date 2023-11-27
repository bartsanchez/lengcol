from django.contrib import auth
from django.contrib.auth import views
from django.views.generic import edit

from authentication import forms


class RegisterView(edit.FormView):
    template_name = "authentication/register.html"
    form_class = forms.CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        user_model = auth.get_user_model()
        user = user_model.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
            email=form.cleaned_data["email"],
        )
        auth.login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(views.LoginView):
    form_class = forms.CustomAuthenticationForm
