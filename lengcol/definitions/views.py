from django import http
from django import shortcuts
from django import urls
from django import views
from django.contrib import auth
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
        return urls.reverse(
            'definition-detail', kwargs={'uuid': self.object.uuid}
        )

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated:
            UserModel = auth.get_user_model()
            definition = form.save(commit=False)
            definition.user = UserModel.objects.get(username=user.username)
            definition.save()
        return super().form_valid(form)


class DefinitionDisplayView(generic.DetailView):
    model = models.Definition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ExampleForm()
        return context

    def get_object(self):
        return shortcuts.get_object_or_404(models.Definition,
                                           uuid=self.kwargs['uuid'])


class ExampleView(detail.SingleObjectMixin, generic.FormView):
    template_name = 'definitions/definition_detail.html'
    form_class = forms.ExampleForm
    model = models.Definition

    def get_object(self):
        return shortcuts.get_object_or_404(models.Definition,
                                           uuid=self.kwargs['uuid'],
                                           user__isnull=False)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        if self.object.user != request.user:
            return http.HttpResponse('Unauthorized', status=401)
        if form.is_valid():
            example, created = models.Example.objects.get_or_create(
                definition=self.object,
                value=form.data['example'],
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return urls.reverse(
            'definition-detail', kwargs={'uuid': self.object.uuid}
        )


class DefinitionDetailView(views.View):
    def get(self, request, *args, **kwargs):
        view = DefinitionDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ExampleView.as_view()
        return view(request, *args, **kwargs)


class TermDetailView(generic.DetailView):
    model = models.Term


class TermSearchView(generic.ListView):
    template_name = 'definitions/term_search.html'
    model = models.Term

    def get_queryset(self):
        term = self.request.GET.get('v', '')
        query = models.Term.objects.all()
        if term:
            query = query.filter(value__icontains=term)
        return query
