from django import forms
from extra_views import InlineFormSetFactory
from snowpenguin.django.recaptcha3 import fields

from definitions import models


class ModelChoiceFieldAsText(forms.ModelChoiceField):
    def __init__(self, queryset, field, *args, **kwargs):
        super().__init__(queryset, *args, **kwargs)
        self.widget = forms.TextInput()
        self.field = field

    def prepare_value(self, value):
        if isinstance(value, int):
            return self.queryset.get(pk=value).value
        return value

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
        to_field_name='value',
    )
    value = forms.CharField(label='Definición', widget=forms.Textarea())

    captcha = fields.ReCaptchaField()

    class Meta:
        model = models.Definition
        exclude = ('user', 'active')

    def clean(self, *args, **kwargs):
        super().clean()
        if not self.is_valid() and 'captcha' in self.errors:
            term = self.cleaned_data['term']
            if term.definitions.count() == 0:
                term.active = False
                term.save()


class ExampleForm(forms.ModelForm):
    value = forms.CharField(label='')

    class Meta:
        model = models.Example
        fields = ('value',)


class ExampleInline(InlineFormSetFactory):
    model = models.Example
    form_class = ExampleForm
    factory_kwargs = {'extra': 2, 'max_num': 5}

    def construct_formset(self):
        formset = super().construct_formset()
        formset.delete_existing = self.delete_existing
        return formset

    def delete_existing(self, obj, commit=True):
        if commit:
            obj.active = False
            obj.save()
