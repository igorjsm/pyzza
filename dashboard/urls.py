from django.urls import path

from .views import DashboardView
from .views_categoria import (
    CategoriaCreateView,
    CategoriaDeleteView,
    CategoriaListView,
    CategoriaUpdateView,
)
from .views_pedido import PedidoListView, PedidoStatusUpdateView
from .views_produto import (
    ProdutoCreateView,
    ProdutoDeleteView,
    ProdutoListView,
    ProdutoUpdateView,
)
from .views_user import UserCreateView, UserDeleteView, UserListView, UserUpdateView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # Usuários
    path("cadastrar-usuario/", UserCreateView.as_view(), name="UserCreateView"),
    path("listar-usuario/", UserListView.as_view(), name="UserListView"),
    path("editar-usuario/<int:pk>/", UserUpdateView.as_view(), name="UserUpdateView"),
    path("deletar-usuario/<int:pk>/", UserDeleteView.as_view(), name="UserDeleteView"),
    # Categorias
    path(
        "cadastrar-categoria/",
        CategoriaCreateView.as_view(),
        name="CategoriaCreateView",
    ),
    path("listar-categoria/", CategoriaListView.as_view(), name="CategoriaListView"),
    path(
        "editar-categoria/<int:pk>/",
        CategoriaUpdateView.as_view(),
        name="CategoriaUpdateView",
    ),
    path(
        "deletar-categoria/<int:pk>/",
        CategoriaDeleteView.as_view(),
        name="CategoriaDeleteView",
    ),
    # Produtos
    path("cadastrar-produto/", ProdutoCreateView.as_view(), name="ProdutoCreateView"),
    path("listar-produto/", ProdutoListView.as_view(), name="ProdutoListView"),
    path(
        "editar-produto/<int:pk>/",
        ProdutoUpdateView.as_view(),
        name="ProdutoUpdateView",
    ),
    path(
        "deletar-produto/<int:pk>/",
        ProdutoDeleteView.as_view(),
        name="ProdutoDeleteView",
    ),
    path("pedidos/", PedidoListView.as_view(), name="pedido_list"),
    path(
        "pedidos/<int:pk>/status/",
        PedidoStatusUpdateView.as_view(),
        name="pedido_status_update",
    ),
]
