from django import http, shortcuts, urls
from django.conf import settings
from django.contrib.auth import mixins
from django.contrib.postgres import search
from django.db.models import functions
from django.views import generic
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from tagging import models as tagging_models

from definitions import forms, models


class IndexView(generic.ListView):
    model = models.Definition
    template_name = "definitions/index.html"
    context_object_name = "definitions"
    paginate_by = 5


class DefinitionCreateView(CreateWithInlinesView):
    model = models.Definition
    form_class = forms.DefinitionForm
    inlines = [forms.ExampleInline]
    template_name = "definitions/create_definition_and_examples.html"

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated:
            form.instance.user = user
        return super().form_valid(form)


class DefinitionDetailView(generic.DetailView):
    model = models.Definition

    def get_object(self):
        return shortcuts.get_object_or_404(models.Definition, uuid=self.kwargs["uuid"])


class DefinitionUpdateView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    UpdateWithInlinesView,
):
    model = models.Definition
    form_class = forms.DefinitionForm
    inlines = [forms.ExampleInline]
    template_name = "definitions/update_definition_and_examples.html"

    def test_func(self):
        user = self.request.user
        definition_user = self.get_object().user
        return user == definition_user

    def get_object(self):
        return shortcuts.get_object_or_404(models.Definition, uuid=self.kwargs["uuid"])


class DefinitionDisableView(generic.edit.DeleteView):
    model = models.Definition
    success_url = urls.reverse_lazy("index")

    def get_object(self):
        user = self.request.user
        return shortcuts.get_object_or_404(
            models.Definition,
            user=user,
            uuid=self.kwargs["uuid"],
        )

    def form_valid(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.active = False
        self.object.save()
        return http.HttpResponseRedirect(success_url)


class TermDetailView(generic.DetailView):
    model = models.Term


class TermSearchView(generic.ListView):
    template_name = "definitions/term_search.html"
    model = models.Term
    paginate_by = 5

    def db_engine_is_sqlite(self):
        return "sqlite" in settings.DATABASES["default"]["ENGINE"]

    def get_queryset(self):
        term = self.request.GET.get("v", "")
        query = models.Term.objects.all()
        if term:
            if self.db_engine_is_sqlite():
                query = models.Term.objects.filter(value__icontains=term)
            else:
                query = (
                    models.Term.objects.annotate(
                        similarity=functions.Greatest(
                            search.TrigramSimilarity("value", term),
                            search.TrigramSimilarity("definition__value", term),
                            search.TrigramSimilarity("definition__tags", term),
                        ),
                    )
                    .filter(similarity__gt=0.1)
                    .order_by("-similarity")
                )
        return query


class DefinitionsByTagView(generic.ListView):
    model = models.Definition
    template_name = "definitions/by_tag.html"
    context_object_name = "definitions"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        tag_name = self.kwargs["tag_name"]
        tag = shortcuts.get_object_or_404(tagging_models.Tag, name=tag_name)
        tagged_items = tagging_models.TaggedItem.objects.get_by_model(
            models.Definition,
            tag,
        )
        return models.Definition.objects.filter(id__in=tagged_items)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_name"] = self.kwargs["tag_name"]
        return context


class TagListView(generic.ListView):
    model = tagging_models.Tag
    template_name = "definitions/tag_list.html"
    context_object_name = "tags"
    paginate_by = 100
