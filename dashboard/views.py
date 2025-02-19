from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
