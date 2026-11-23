from decimal import Decimal

from django import forms

from .models import Cliente, ItemEstoque, MovimentacaoEstoque, Pedido


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

        fields = [
            "nome",
            "telefone",
            "cep",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "uf",
            "observacoes",
        ]

        widgets = {
            "telefone": forms.TextInput(
                attrs={"type": "tel"}
            ),
            "cep": forms.TextInput(
                attrs={"placeholder": "00000-000"}
            ),            
            "uf": forms.Select(
                choices=[
                    ("", "Selecione um estado"),
                    ("AC", "Acre"),
                    ("AL", "Alagoas"),
                    ("AP", "Amapá"),
                    ("AM", "Amazonas"),
                    ("BA", "Bahia"),
                    ("CE", "Ceará"),
                    ("DF", "Distrito Federal"),
                    ("ES", "Espírito Santo"),
                    ("GO", "Goiás"),
                    ("MA", "Maranhão"),
                    ("MT", "Mato Grosso"),
                    ("MS", "Mato Grosso do Sul"),
                    ("MG", "Minas Gerais"),
                    ("PA", "Pará"),
                    ("PB", "Paraíba"),
                    ("PR", "Paraná"),
                    ("PE", "Pernambuco"),
                    ("PI", "Piauí"),
                    ("RJ", "Rio de Janeiro"),
                    ("RN", "Rio Grande do Norte"),
                    ("RS", "Rio Grande do Sul"),
                    ("RO", "Rondônia"),
                    ("RR", "Roraima"),
                    ("SC", "Santa Catarina"),
                    ("SP", "São Paulo"),
                    ("SE", "Sergipe"),
                    ("TO", "Tocantins"),
                ]
            ),

            "observacoes": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

    def clean_cep(self):
        import re

        cep = self.cleaned_data["cep"].strip()

        if not cep:
            return ""

        if not re.fullmatch(r"\d{5}-?\d{3}", cep):
            raise forms.ValidationError(
                "Informe um CEP com 8 dígitos."
            )

        numeros = cep.replace("-", "")
        return f"{numeros[:5]}-{numeros[5:]}"

    def clean_uf(self):
        uf = self.cleaned_data["uf"].strip().upper()

        ufs_validas = {
            "AC", "AL", "AP", "AM", "BA", "CE",
            "DF", "ES", "GO", "MA", "MT", "MS",
            "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC",
            "SP", "SE", "TO",
        }

        if uf and uf not in ufs_validas:
            raise forms.ValidationError(
                "Informe uma UF brasileira válida."
            )

        return uf


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
