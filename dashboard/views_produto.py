from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from cardapio.models import Produto

from .forms import ProdutoForm


class ProdutoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "dashboard/produto/cadastrar.html"
    success_url = reverse_lazy("ProdutoListView")
    success_message = "Produto cadastrado com sucesso."


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "dashboard/produto/listar.html"
    context_object_name = "produtos"
    paginate_by = 10

    def get_queryset(self):
        queryset = Produto.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(nome__icontains=search_query) | Q(descricao__icontains=search_query)
            )
        sort_by = self.request.GET.get("sort", "id")
        order = self.request.GET.get("order", "asc")
        if order == "desc":
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)
        return queryset


class ProdutoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "dashboard/produto/editar.html"
    success_url = reverse_lazy("ProdutoListView")
    success_message = "Produto atualizado com sucesso."


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "dashboard/produto/deletar.html"
    success_url = reverse_lazy("ProdutoListView")
