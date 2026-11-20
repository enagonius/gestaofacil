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
