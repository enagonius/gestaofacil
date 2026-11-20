from django import forms

from .models import Cliente, Pedido


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "telefone", "observacoes"]
        widgets = {
            "telefone": forms.TextInput(attrs={"type": "tel"}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }


class PedidoForm(forms.ModelForm):
    quantidade = forms.IntegerField(min_value=1, max_value=2147483647, initial=1)

    class Meta:
        model = Pedido
        fields = ["cliente", "descricao", "quantidade", "data_entrega", "observacoes"]
        widgets = {
            "data_entrega": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }
