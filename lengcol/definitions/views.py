from django import http, shortcuts, urls
from django.contrib.auth import mixins
from django.views import generic
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from definitions import forms, models


class IndexView(generic.ListView):
    model = models.Definition
    template_name = 'definitions/index.html'
    context_object_name = 'definitions'
    paginate_by = 5


class DefinitionCreateView(CreateWithInlinesView):
    model = models.Definition
    form_class = forms.DefinitionForm
    inlines = [forms.ExampleInline]
    template_name = 'definitions/create_definition_and_examples.html'

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated:
            form.instance.user = user
        return super().form_valid(form)


class DefinitionDetailView(generic.DetailView):
    model = models.Definition

    def get_object(self):
        return shortcuts.get_object_or_404(models.Definition,
                                           uuid=self.kwargs['uuid'])


class DefinitionUpdateView(mixins.LoginRequiredMixin,
                           mixins.UserPassesTestMixin,
                           UpdateWithInlinesView):
    model = models.Definition
    form_class = forms.DefinitionForm
    inlines = [forms.ExampleInline]
    template_name = 'definitions/update_definition_and_examples.html'

    def test_func(self):
        user = self.request.user
        definition_user = self.get_object().user
        return user == definition_user

    def get_object(self):
        return shortcuts.get_object_or_404(models.Definition,
                                           uuid=self.kwargs['uuid'])


class DefinitionDisableView(generic.edit.DeleteView):
    model = models.Definition
    success_url = urls.reverse_lazy('index')

    def get_object(self):
        user = self.request.user
        return shortcuts.get_object_or_404(models.Definition,
                                           user=user,
                                           uuid=self.kwargs['uuid'])

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.active = False
        self.object.save()
        return http.HttpResponseRedirect(success_url)


class TermDetailView(generic.DetailView):
    model = models.Term


class TermSearchView(generic.ListView):
    template_name = 'definitions/term_search.html'
    model = models.Term
    paginate_by = 5

    def get_queryset(self):
        term = self.request.GET.get('v', '')
        query = models.Term.objects.all()
        if term:
            query = query.filter(value__icontains=term)
        return query
