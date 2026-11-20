from decimal import Decimal

from django import forms

from .models import Cliente, ItemEstoque, MovimentacaoEstoque, Pedido


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


class ItemEstoqueForm(forms.ModelForm):
    estoque_minimo = forms.DecimalField(
        label="Estoque mínimo", min_value=0, max_digits=12,
        decimal_places=3, localize=True, initial=0,
        help_text="O alerta aparece quando o saldo atinge esse valor.",
    )

    class Meta:
        model = ItemEstoque
        fields = ["nome", "unidade", "estoque_minimo"]


class MovimentacaoForm(forms.Form):
    tipo = forms.ChoiceField(label="Operação", choices=MovimentacaoEstoque.Tipo.choices)
    quantidade = forms.DecimalField(
        min_value=Decimal("0.001"), max_digits=12, decimal_places=3, localize=True,
    )
    observacoes = forms.CharField(
        label="Observações", max_length=500, required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    chave_operacao = forms.UUIDField(widget=forms.HiddenInput)
