from django import urls
from django import views
from django.views import generic
from django.views.generic import detail

from definitions import forms
from definitions import models


class IndexView(generic.ListView):
    model = models.Definition
    template_name = 'definitions/index.html'
    context_object_name = 'definitions'


class DefinitionCreateView(generic.CreateView):
    model = models.Definition
    form_class = forms.DefinitionForm

    def get_success_url(self):
        return urls.reverse('definition-detail', kwargs={'pk': self.object.pk})


class DefinitionDisplayView(generic.DetailView):
    model = models.Definition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ExampleForm()
        return context


class ExampleView(detail.SingleObjectMixin, generic.FormView):
    template_name = 'definitions/definition_detail.html'
    form_class = forms.ExampleForm
    model = models.Definition

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            example, created = models.Example.objects.get_or_create(
                definition=self.object,
                value=form.data['example'],
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return urls.reverse('definition-detail', kwargs={'pk': self.object.pk})


class DefinitionDetailView(views.View):
    def get(self, request, *args, **kwargs):
        view = DefinitionDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ExampleView.as_view()
        return view(request, *args, **kwargs)


class TermDetailView(generic.DetailView):
    model = models.Term
