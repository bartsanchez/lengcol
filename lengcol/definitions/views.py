from django import urls
from django.views import generic

from definitions import forms
from definitions import models


class IndexView(generic.ListView):
    model = models.Term
    template_name = 'definitions/index.html'
    context_object_name = 'terms'


class DefinitionCreateView(generic.CreateView):
    model = models.Definition
    form_class = forms.DefinitionForm
    success_url = urls.reverse_lazy('index')


class DefinitionDetailView(generic.DetailView):
    model = models.Definition
