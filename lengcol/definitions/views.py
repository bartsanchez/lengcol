from django.views import generic
from definitions import models


class IndexView(generic.ListView):
    model = models.Term
    template_name = 'definitions/index.html'
    context_object_name = 'terms'
