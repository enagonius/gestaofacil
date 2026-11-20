from datetime import date
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, ItemEstoque, MovimentacaoEstoque, Pedido


class FluxosGestaoFacilTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(username="teste", password="senha-local-de-teste")
        cls.cliente = Cliente.objects.create(nome="Ana Costa")
        cls.item = ItemEstoque.objects.create(
            nome="Farinha de trigo", unidade="KG", estoque_minimo_milesimos=2000,
        )

    def setUp(self):
        self.client.force_login(self.usuario)

    def test_painel_exige_login(self):
        self.client.logout()
        resposta = self.client.get(reverse("painel"))
        self.assertRedirects(resposta, reverse("login") + "?next=/")

    def test_cadastra_cliente_e_valida_nome(self):
        rota = reverse("cliente_novo")
        resposta = self.client.post(rota, {"nome": "  "})
        self.assertTrue(resposta.context["form"].errors.get("nome"))
        resposta = self.client.post(rota, {"nome": "Cliente de teste", "telefone": "123"})
        pessoa = Cliente.objects.get(nome="Cliente de teste")
        self.assertRedirects(resposta, reverse("cliente_detalhe", args=[pessoa.pk]))

    def test_pedido_aparece_no_historico_e_nao_avanca_duas_vezes(self):
        dados = {
            "cliente": self.cliente.pk, "descricao": "Bolo de chocolate", "quantidade": 1,
            "data_entrega": date(2026, 12, 5).isoformat(),
        }
        self.client.post(reverse("pedido_novo"), dados)
        pedido = Pedido.objects.get(descricao="Bolo de chocolate")
        rota = reverse("pedido_status", args=[pedido.pk])
        self.client.post(rota, {"status_atual": "PENDENTE"})
        self.client.post(rota, {"status_atual": "PENDENTE"})
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, Pedido.Status.EM_PRODUCAO)
        resposta = self.client.get(reverse("cliente_detalhe", args=[self.cliente.pk]))
        self.assertContains(resposta, "Bolo de chocolate")
        self.assertContains(resposta, "Em produção")

    def test_saida_atinge_minimo_e_repeticao_preserva_o_saldo(self):
        rota = reverse("estoque_detalhe", args=[self.item.pk])
        self.client.post(rota, {"tipo": "ENTRADA", "quantidade": "5", "chave_operacao": uuid4()})
        saida = {"tipo": "SAIDA", "quantidade": "3", "chave_operacao": uuid4()}
        self.client.post(rota, saida)
        self.client.post(rota, saida)
        resposta = self.client.post(rota, saida | {"chave_operacao": uuid4()})
        self.assertContains(resposta, "Saldo insuficiente")
        self.item.refresh_from_db()
        self.assertEqual(self.item.saldo_milesimos, 2000)
        self.assertEqual(MovimentacaoEstoque.objects.filter(item=self.item).count(), 2)
        self.assertContains(self.client.get(reverse("painel")), "Estoque baixo")

    def test_quantidade_decimal_com_virgula(self):
        rota = reverse("estoque_detalhe", args=[self.item.pk])
        resposta = self.client.post(
            rota, {"tipo": "ENTRADA", "quantidade": "0,250", "chave_operacao": uuid4()},
        )
        self.assertRedirects(resposta, rota)
        self.item.refresh_from_db()
        self.assertEqual(self.item.saldo_milesimos, 250)
