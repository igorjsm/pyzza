from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="produtos"
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Aguardando Confirmação", "Aguardando Confirmação"),
        ("Em Preparo", "Em Preparo"),
        ("Saiu para Entrega", "Saiu para Entrega"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    endereco = models.TextField()
    forma_pagamento = models.CharField(max_length=20)
    troco_para = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pendente")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"
