from django import forms

from .models import Pedido


class FinalizarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["endereco", "forma_pagamento", "troco_para"]
        widgets = {
            "endereco": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Informe seu endereço"}
            ),
            "forma_pagamento": forms.Select(attrs={"class": "form-control"}),
            "troco_para": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Se necessário, informe o valor",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        forma_pagamento = cleaned_data.get("forma_pagamento")
        troco_para = cleaned_data.get("troco_para")

        if forma_pagamento == "Dinheiro" and not troco_para:
            self.add_error("troco_para", "Informe o valor para troco.")

        return cleaned_data
