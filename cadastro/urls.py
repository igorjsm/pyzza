from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path

from .views import (
    ActivateAccountView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    LoginView,
    LogoutView,
    PasswordResetView,
    RegisterView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("cadastrar-se/", RegisterView.as_view(), name="cadastrar_se"),
    path("recuperar-senha/", CustomPasswordResetView.as_view(), name="recuperar_senha"),
    path(
        "ativar-conta/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="ativar_conta",
    ),
    path(
        "recuperar-senha/confirmar/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="recuperar_senha_confirmar",
    ),
    path(
        "recuperar-senha/completo/",
        PasswordResetCompleteView.as_view(
            template_name="cadastro/recuperar_senha_completo.html"
        ),
        name="recuperar_senha_completo",
    ),
]
