import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError

from cardapio.models import Categoria, Produto


class CustomUserCreateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Nome de usuário", "class": "form-control"}
        ),
        label="Nome de usuário",
        help_text="Obrigatório. 150 caracteres ou menos. Letras, algarismos e @/./+/-/_ apenas.",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
            "max_length": "Certifique-se de que este valor tenha no máximo 150 caracteres.",
        },
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
        label="Email",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Senha", "class": "form-control"}
        ),
        label="Senha",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
        },
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirme sua senha", "class": "form-control"}
        ),
        label="Confirmação da senha",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
        },
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Grupos",
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        error_messages={"required": "Selecione pelo menos um grupo para o usuário."},
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "groups"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and password != confirm_password:
            raise ValidationError({"confirm_password": "As senhas não coincidem."})
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
            user.groups.set(self.cleaned_data.get("groups"))
        return user


class CustomUserUpdateForm(CustomUserCreateForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Senha", "class": "form-control"}
        ),
        label="Senha",
        help_text="Deixe este campo vazio para manter a senha atual.",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
        },
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirme sua senha", "class": "form-control"}
        ),
        label="Confirmação da senha",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
        },
    )


class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Nome da categoria", "class": "form-control"}
        ),
        label="Nome da Categoria",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Forneça um valor válido.",
            "blank": "Este campo não pode ficar vazio.",
            "null": "Este campo não pode ser nulo.",
            "max_length": "Certifique-se de que este valor tenha no máximo 255 caracteres.",
        },
    )

    class Meta:
        model = Categoria
        fields = ["nome"]


class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Nome do produto", "class": "form-control"}
        ),
        label="Nome do Produto",
        error_messages={
            "required": "Este campo é obrigatório.",
            "max_length": "Certifique-se de que este valor tenha no máximo 255 caracteres.",
        },
    )

    descricao = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Descrição do produto",
                "class": "form-control",
                "rows": 3,
            }
        ),
        label="Descrição",
        required=False,
    )

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Categoria",
        error_messages={"required": "Selecione uma categoria."},
    )

    preco = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Preço", "class": "form-control", "step": "0.01"}
        ),
        label="Preço",
        max_digits=10,
        decimal_places=2,
    )

    imagem = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label="Imagem do Produto",
        required=False,
        error_messages={"invalid": "Forneça um arquivo de imagem válido."},
    )

    class Meta:
        model = Produto
        fields = ["nome", "descricao", "categoria", "preco", "imagem"]
