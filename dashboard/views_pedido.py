from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from cardapio.models import Pedido


class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "dashboard/pedido/listar.html"
    context_object_name = "pedidos"
    ordering = ["-data_criacao"]


class PedidoStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    fields = ["status"]
    template_name = "dashboard/pedido/editar.html"

    def form_valid(self, form):
        pedido = form.save()
        messages.success(
            self.request,
            f"Status do pedido {pedido.id} atualizado para {pedido.get_status_display()}.",
        )
        return redirect("pedido_list")
