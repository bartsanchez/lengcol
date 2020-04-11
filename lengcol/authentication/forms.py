from django import forms
from django.contrib import auth
from django.contrib.auth import forms as auth_forms
from snowpenguin.django.recaptcha3 import fields


class CustomUserCreationForm(auth_forms.UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    email = forms.EmailField()

    captcha = fields.ReCaptchaField()

    class Meta:
        model = auth.get_user_model()
        fields = ('username', 'password1', 'password2', 'email')
        field_classes = {'username': auth_forms.UsernameField}
