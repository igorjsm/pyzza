from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView

from .forms import FinalizarPedidoForm
from .models import Categoria, ItemPedido, Pedido, Produto


class CardapioListView(ListView):
    model = Produto
    template_name = "cardapio/cardapio.html"
    context_object_name = "produtos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context


class AdicionarAoPedidoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        produto = get_object_or_404(Produto, id=self.kwargs["produto_id"])

        pedido, created = Pedido.objects.get_or_create(
            cliente=request.user, status="Pendente"
        )

        item_pedido, item_created = ItemPedido.objects.get_or_create(
            pedido=pedido, produto=produto, defaults={"quantidade": 1}
        )

        if not item_created:
            item_pedido.quantidade += 1
            item_pedido.save()

        messages.success(request, f"{produto.nome} adicionado ao seu pedido!")

        return redirect("meu_pedido")


class MeuPedidoView(LoginRequiredMixin, View):
    def get(self, request):
        pedido = Pedido.objects.filter(cliente=request.user, status="Pendente").first()
        itens = pedido.itens.all() if pedido else []

        form = FinalizarPedidoForm()

        return render(
            request,
            "cardapio/meu_pedido.html",
            {
                "pedido": pedido,
                "itens": itens,
                "form": form,
            },
        )

    def post(self, request):
        pedido = Pedido.objects.filter(cliente=request.user, status="Pendente").first()

        if not pedido:
            messages.error(request, "Você não tem um pedido aberto.")
            return redirect("meu_pedido")

        if "remover_item" in request.POST:
            item_id = request.POST.get("remover_item")
            item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)
            item.delete()
            messages.success(request, f"Item {item.produto.nome} removido do pedido.")
            return redirect("meu_pedido")

        if "atualizar_quantidade" in request.POST:
            item_id = request.POST.get("item_id")
            nova_quantidade = int(request.POST.get("quantidade", 1))
            item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)

            if nova_quantidade > 0:
                item.quantidade = nova_quantidade
                item.save()
                messages.success(
                    request, f"Quantidade de {item.produto.nome} atualizada."
                )
            else:
                item.delete()
                messages.success(request, f"Item {item.produto.nome} removido.")

            return redirect("meu_pedido")

        if "finalizar_pedido" in request.POST:
            form = FinalizarPedidoForm(request.POST)
            if form.is_valid():
                pedido.endereco = form.cleaned_data["endereco"]
                pedido.forma_pagamento = form.cleaned_data["forma_pagamento"]
                pedido.troco_para = form.cleaned_data["troco_para"]
                pedido.status = "Em Preparo"
                pedido.save()
                messages.success(request, "Pedido finalizado com sucesso!")
                return redirect("ver_pedidos")

            messages.error(request, "Preencha todos os campos para finalizar o pedido.")

        return redirect("meu_pedido")


class VerPedidosView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "cardapio/ver_pedidos.html"
    context_object_name = "pedidos"

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user).order_by(
            "-data_criacao"
        )
