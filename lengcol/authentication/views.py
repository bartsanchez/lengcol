from authentication import forms
from django.contrib import auth
from django.contrib.auth import views
from django.views.generic import edit


class RegisterView(edit.FormView):
    template_name = "authentication/register.html"
    form_class = forms.CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        User = auth.get_user_model()
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
            email=form.cleaned_data["email"],
        )
        auth.login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(views.LoginView):
    form_class = forms.CustomAuthenticationForm
