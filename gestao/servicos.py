from django.db import IntegrityError, transaction
from django.db.models import F

from .models import MAXIMO_MILESIMOS, ItemEstoque, MovimentacaoEstoque


def registrar_movimentacao(item, dados):
    """Recebe dados validados pelo formulário e devolve o resultado da operação."""
    quantidade = int(dados["quantidade"] * 1000)
    chave = dados["chave_operacao"]
    registros = MovimentacaoEstoque.objects.filter(item=item, chave_operacao=chave)
    itens = ItemEstoque.objects.filter(pk=item.pk)

    try:
        with transaction.atomic():
            # A primeira consulta dentro da transação é a atualização do saldo.
            # A condição é conferida pelo banco junto com a escrita.
            if dados["tipo"] == MovimentacaoEstoque.Tipo.SAIDA:
                alterados = itens.filter(saldo_milesimos__gte=quantidade).update(
                    saldo_milesimos=F("saldo_milesimos") - quantidade,
                )
                erro = "saldo_insuficiente"
            else:
                alterados = itens.filter(saldo_milesimos__lte=MAXIMO_MILESIMOS - quantidade).update(
                    saldo_milesimos=F("saldo_milesimos") + quantidade,
                )
                erro = "limite_excedido"

            if alterados:
                MovimentacaoEstoque.objects.create(
                    item=item, tipo=dados["tipo"], quantidade_milesimos=quantidade,
                    observacoes=dados["observacoes"], chave_operacao=chave,
                )
                return "registrada"
    except IntegrityError:
        # Uma chave repetida cancela também a alteração do saldo na transação.
        if registros.exists():
            return "ja_registrada"
        raise

    return "ja_registrada" if registros.exists() else erro
