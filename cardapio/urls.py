from django.urls import path

from .views import (
    AdicionarAoPedidoView,
    CardapioListView,
    MeuPedidoView,
    VerPedidosView,
)

urlpatterns = [
    path("cardapio/", CardapioListView.as_view(), name="cardapio"),
    path(
        "adicionar-ao-pedido/<int:produto_id>/",
        AdicionarAoPedidoView.as_view(),
        name="adicionar_ao_pedido",
    ),
    path("meu-pedido/", MeuPedidoView.as_view(), name="meu_pedido"),
    path("ver-pedidos/", VerPedidosView.as_view(), name="ver_pedidos"),
]
