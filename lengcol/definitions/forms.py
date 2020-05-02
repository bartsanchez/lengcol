from django import forms
from snowpenguin.django.recaptcha3 import fields

from definitions import models


class ModelChoiceFieldAsText(forms.ModelChoiceField):
    def __init__(self, queryset, field, *args, **kwargs):
        super().__init__(queryset, *args, **kwargs)
        self.widget = forms.TextInput()
        self.field = field

    def to_python(self, value):
        if value in self.empty_values:
            return None

        obj, created = self.queryset.get_or_create(**{self.field: value})

        return obj


class DefinitionForm(forms.ModelForm):
    term = ModelChoiceFieldAsText(
        queryset=models.Term.objects.all(),
        field='value',
        label='Término',
    )
    value = forms.CharField(label='Definición')
    example = forms.CharField(label='Ejemplo', required=False)

    captcha = fields.ReCaptchaField()

    class Meta:
        model = models.Definition
        exclude = ('user', 'active')

    def save(self, *args, **kwargs):
        return_value = super().save(*args, **kwargs)
        if self.is_valid():
            example = self.cleaned_data['example']
            if example:
                obj, created = models.Example.objects.get_or_create(
                    definition=self.instance,
                    value=example,
                )
        return return_value


class ExampleForm(forms.Form):
    example = forms.CharField(label='Ejemplo')
