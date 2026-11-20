from decimal import Decimal

from django.db import models


class Cliente(models.Model):
    nome = models.CharField("nome", max_length=120)
    telefone = models.CharField("telefone", max_length=30, blank=True)
    observacoes = models.TextField("observações", max_length=500, blank=True)

    class Meta:
        db_table = "cliente"
        ordering = ["nome", "id"]

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_PRODUCAO = "EM_PRODUCAO", "Em produção"
        FINALIZADO = "FINALIZADO", "Finalizado"

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="pedidos")
    descricao = models.CharField("descrição do pedido", max_length=160)
    quantidade = models.PositiveIntegerField(default=1)
    data_entrega = models.DateField("data de entrega")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    observacoes = models.TextField("observações", max_length=500, blank=True)

    class Meta:
        db_table = "pedido"
        ordering = ["data_entrega", "id"]
        constraints = [
            models.CheckConstraint(condition=models.Q(quantidade__gt=0), name="pedido_qtd_positiva"),
            models.CheckConstraint(
                condition=models.Q(status__in=["PENDENTE", "EM_PRODUCAO", "FINALIZADO"]),
                name="pedido_status_valido",
            ),
        ]

    @property
    def proximo_status(self):
        return {
            self.Status.PENDENTE: self.Status.EM_PRODUCAO,
            self.Status.EM_PRODUCAO: self.Status.FINALIZADO,
        }.get(self.status)

    def __str__(self):
        return self.descricao


MAXIMO_MILESIMOS = 999_999_999_999


class ItemEstoque(models.Model):
    class Unidade(models.TextChoices):
        KG = "KG", "kg"
        G = "G", "g"
        L = "L", "L"
        ML = "ML", "mL"
        UN = "UN", "un."

    nome = models.CharField(max_length=120)
    unidade = models.CharField(max_length=2, choices=Unidade.choices)
    saldo_milesimos = models.PositiveBigIntegerField(default=0)
    estoque_minimo_milesimos = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "item_estoque"
        ordering = ["nome", "id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(saldo_milesimos__lte=MAXIMO_MILESIMOS),
                name="item_saldo_maximo",
            ),
        ]

    @property
    def saldo(self):
        return Decimal(self.saldo_milesimos) / 1000

    @property
    def estoque_minimo(self):
        return Decimal(self.estoque_minimo_milesimos) / 1000

    @property
    def estoque_baixo(self):
        return self.saldo_milesimos <= self.estoque_minimo_milesimos

    def __str__(self):
        return self.nome


class MovimentacaoEstoque(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"

    item = models.ForeignKey(ItemEstoque, on_delete=models.PROTECT, related_name="movimentacoes")
    tipo = models.CharField(max_length=7, choices=Tipo.choices)
    quantidade_milesimos = models.PositiveBigIntegerField()
    criada_em = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField("observações", max_length=500, blank=True)
    chave_operacao = models.UUIDField()

    class Meta:
        db_table = "movimentacao_estoque"
        ordering = ["-criada_em", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade_milesimos__gt=0),
                name="movimentacao_qtd_positiva",
            ),
            models.UniqueConstraint(fields=["item", "chave_operacao"], name="movimentacao_chave_unica"),
        ]

    @property
    def quantidade(self):
        return Decimal(self.quantidade_milesimos) / 1000
