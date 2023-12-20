from django.conf import settings
from django.views.generic import base


class RobotsTxtView(base.TemplateView):
    template_name = "lengcol/robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_url"] = settings.BASE_URL
        return context
