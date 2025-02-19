from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from cardapio.models import Categoria

from .forms import CategoriaForm


class CategoriaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "dashboard/categoria/cadastrar.html"
    success_url = reverse_lazy("CategoriaListView")
    success_message = "Categoria cadastrada com sucesso."


class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = "dashboard/categoria/listar.html"
    context_object_name = "categorias"
    paginate_by = 10

    def get_queryset(self):
        queryset = Categoria.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        sort_by = self.request.GET.get("sort", "id")
        order = self.request.GET.get("order", "asc")
        if order == "desc":
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)
        return queryset


class CategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "dashboard/categoria/editar.html"
    success_url = reverse_lazy("CategoriaListView")
    success_message = "Categoria atualizada com sucesso."


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = "dashboard/categoria/deletar.html"
    success_url = reverse_lazy("CategoriaListView")
