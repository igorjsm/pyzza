from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CustomUserCreateForm, CustomUserUpdateForm


class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreateForm
    template_name = "dashboard/user/cadastrar.html"
    success_url = reverse_lazy("UserListView")
    success_message = "Usuário cadastrado com sucesso."


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "dashboard/user/listar.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) | Q(email__icontains=search_query)
            )
        sort_by = self.request.GET.get("sort", "id")
        order = self.request.GET.get("order", "asc")
        if order == "desc":
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)
        return queryset


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = "dashboard/user/editar.html"
    success_url = reverse_lazy("UserListView")
    success_message = "Usuário atualizado com sucesso."


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "dashboard/user/deletar.html"
    success_url = reverse_lazy("UserListView")
