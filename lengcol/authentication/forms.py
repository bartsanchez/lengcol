from django.contrib import auth
from django.contrib.auth import forms


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = auth.get_user_model()
        fields = ("username",)
        field_classes = {'username': forms.UsernameField}
