# Generated by Django 5.1.3 on 2025-02-19 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardapio', '0004_alter_pedido_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='endereco_entrega',
            field=models.TextField(default='Rua Rio de Janeiro, 55'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='metodo_pagamento',
            field=models.CharField(choices=[('Dinheiro', 'Dinheiro'), ('Cartão', 'Cartão'), ('Pix', 'Pix')], default='Pix', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='troco_para',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Em Preparo', 'Em Preparo'), ('Saiu para Entrega', 'Saiu para Entrega'), ('Entregue', 'Entregue'), ('Cancelado', 'Cancelado')], default='Pendente', max_length=20),
        ),
    ]
