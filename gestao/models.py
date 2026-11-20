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
