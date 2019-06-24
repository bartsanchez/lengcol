from django import forms

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

    class Meta:
        model = models.Definition
        fields = '__all__'


class ExampleForm(forms.Form):
    example = forms.CharField()
