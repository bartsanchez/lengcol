from django import forms
from django.contrib import auth
from django.contrib.auth import forms as auth_forms


class CustomUserCreationForm(auth_forms.UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = auth.get_user_model()
        fields = ('username', 'password1', 'password2', 'email')
        field_classes = {'username': auth_forms.UsernameField}
