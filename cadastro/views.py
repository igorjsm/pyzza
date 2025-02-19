from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, View

from .forms import (
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomUserCreationForm,
)


class LoginView(LoginView):
    template_name = "cadastro/login.html"
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name="Cliente").exists():
            return reverse_lazy("cardapio")

        return reverse_lazy("dashboard")


class LogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def get_next_page(self):
        return reverse_lazy("login")


class RegisterView(CreateView):
    template_name = "cadastro/cadastrar_se.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        grupo_cliente, created = Group.objects.get_or_create(name="Cliente")
        user.groups.add(grupo_cliente)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse_lazy("ativar_conta", kwargs={"uidb64": uid, "token": token})
        )

        send_mail(
            subject="Confirme seu e-mail",
            message=f"Olá {user.username},\n\nClique no link para ativar sua conta: {activation_link}",
            from_email="no-reply@pyzza.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return render(self.request, "cadastro/confirmacao_enviada.html")


class CustomPasswordResetView(PasswordResetView):
    template_name = "cadastro/recuperar_senha.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = self.request.build_absolute_uri(
                reverse_lazy(
                    "recuperar_senha_confirmar", kwargs={"uidb64": uid, "token": token}
                )
            )

            send_mail(
                subject="Redefinição de Senha",
                message=f"Olá {user.username},\n\nClique no link para redefinir sua senha: {reset_link}",
                from_email="seuemail@exemplo.com",
                recipient_list=[user.email],
            )

        return render(self.request, "cadastro/recuperar_senha_sucesso.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("login")

        return render(
            request,
            "cadastro/ativacao_invalida.html",
            {"error": "O link de ativação é inválido ou expirou."},
        )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "cadastro/definir_nova_senha.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("recuperar_senha_completo")
