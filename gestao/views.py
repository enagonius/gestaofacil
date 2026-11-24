from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm, ItemEstoqueForm, MovimentacaoForm, PedidoForm
from .models import Cliente, ItemEstoque, Pedido
from .servicos import registrar_movimentacao



@login_required
def painel(request):
    itens_reposicao = ItemEstoque.objects.filter(
        saldo_milesimos__lte=F("estoque_minimo_milesimos")
    )

    pedidos_abertos = (
        Pedido.objects.exclude(status=Pedido.Status.FINALIZADO)
        .select_related("cliente")[:6]
    )

    contexto = {
        "total_clientes": Cliente.objects.count(),

        "total_pendentes": Pedido.objects.filter(
            status=Pedido.Status.PENDENTE
        ).count(),

        "total_em_producao": Pedido.objects.filter(
            status=Pedido.Status.EM_PRODUCAO
        ).count(),

        "total_estoque_baixo": itens_reposicao.count(),

        "pedidos": pedidos_abertos,
        "itens": itens_reposicao[:6],
    }

    return render(request, "painel.html", contexto)


@login_required
def clientes_lista(request):
    busca = request.GET.get("q", "").strip()[:100]
    clientes = Cliente.objects.all()

    if busca:
        clientes = clientes.filter(
            Q(nome__icontains=busca) | Q(telefone__icontains=busca)
        )

    pagina = Paginator(clientes, 10).get_page(request.GET.get("page"))
    return render(request, "clientes/lista.html", {
        "clientes": pagina,
        "page_obj": pagina,
        "busca": busca,
    })


@login_required
def cliente_form(request, pk=None):
    cliente = get_object_or_404(Cliente, pk=pk) if pk is not None else None
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            salvo = form.save()
            messages.success(request, "Cliente salvo.")
            return redirect("cliente_detalhe", pk=salvo.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "clientes/form.html", {"form": form, "cliente": cliente})


@login_required
def cliente_detalhe(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, "clientes/detalhe.html", {"cliente": cliente, "pedidos": cliente.pedidos.all()})


@login_required
def pedidos_lista(request):
    busca = request.GET.get("q", "").strip()[:100]
    status = request.GET.get("status", "")
    if status not in Pedido.Status.values:
        status = ""

    pedidos = Pedido.objects.select_related("cliente")
    if busca:
        pedidos = pedidos.filter(
            Q(descricao__icontains=busca) | Q(cliente__nome__icontains=busca)
        )
    if status:
        pedidos = pedidos.filter(status=status)

    pagina = Paginator(pedidos, 10).get_page(request.GET.get("page"))
    return render(request, "pedidos/lista.html", {
        "pedidos": pagina,
        "page_obj": pagina,
        "busca": busca,
        "status_selecionado": status,
    })


@login_required
def pedido_form(request, pk=None):
    pedido = get_object_or_404(Pedido, pk=pk) if pk is not None else None
    if pedido is not None and not pedido.proximo_status:
        messages.info(request, "O pedido foi finalizado.")
        return redirect("pedido_detalhe", pk=pedido.pk)
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            if pedido is None:
                pedido = form.save()
            else:
                campos = form.cleaned_data
                alterados = Pedido.objects.filter(pk=pk).exclude(
                    status=Pedido.Status.FINALIZADO
                ).update(**campos)
                if not alterados:
                    messages.warning(request, "O pedido já foi finalizado.")
                    return redirect("pedido_detalhe", pk=pk)
            messages.success(request, "Pedido salvo.")
            return redirect("pedido_detalhe", pk=pedido.pk)
    else:
        cliente = request.GET.get("cliente", "")
        initial = {}
        if pedido is None and cliente.isascii() and cliente.isdigit() and len(cliente) <= 18:
            initial["cliente"] = int(cliente)
        form = PedidoForm(instance=pedido, initial=initial)
    return render(request, "pedidos/form.html", {
        "form": form, "pedido": pedido, "tem_clientes": Cliente.objects.exists(),
    })


@login_required
def pedido_detalhe(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related("cliente"), pk=pk)
    return render(request, "pedidos/detalhe.html", {"pedido": pedido})


@login_required
@require_POST
def pedido_status(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    esperado = request.POST.get("status_atual")
    proximo = pedido.proximo_status
    if proximo and esperado == pedido.status and Pedido.objects.filter(pk=pk, status=esperado).update(status=proximo):
        messages.success(request, "Status atualizado.")
    else:
        messages.info(request, "O status já mudou ou o pedido foi finalizado.")
    return redirect("pedido_detalhe", pk=pk)


@login_required
def estoque_lista(request):
    busca = request.GET.get("q", "").strip()[:100]
    situacao = request.GET.get("situacao", "")
    if situacao not in {"baixo", "normal"}:
        situacao = ""

    itens = ItemEstoque.objects.all()
    if busca:
        itens = itens.filter(nome__icontains=busca)
    if situacao == "baixo":
        itens = itens.filter(
            saldo_milesimos__lte=F("estoque_minimo_milesimos")
        )
    elif situacao == "normal":
        itens = itens.filter(
            saldo_milesimos__gt=F("estoque_minimo_milesimos")
        )

    pagina = Paginator(itens, 10).get_page(request.GET.get("page"))
    return render(request, "estoque/lista.html", {
        "itens": pagina,
        "page_obj": pagina,
        "busca": busca,
        "situacao_selecionada": situacao,
    })


@login_required
def estoque_novo(request):
    if request.method == "POST":
        form = ItemEstoqueForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.estoque_minimo_milesimos = int(form.cleaned_data["estoque_minimo"] * 1000)
            item.save()
            messages.success(request, "Item criado. Registre uma entrada para informar o saldo inicial.")
            return redirect("estoque_detalhe", pk=item.pk)
    else:
        form = ItemEstoqueForm()
    return render(request, "estoque/form.html", {"form": form})


@login_required
def estoque_detalhe(request, pk):
    item = get_object_or_404(ItemEstoque, pk=pk)
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            resultado = registrar_movimentacao(item, form.cleaned_data)
            if resultado == "registrada":
                messages.success(request, "Movimentação registrada.")
                return redirect("estoque_detalhe", pk=pk)
            if resultado == "ja_registrada":
                messages.info(request, "Esta movimentação já está no histórico.")
                return redirect("estoque_detalhe", pk=pk)
            aviso = "Saldo insuficiente para esta saída."
            if resultado == "limite_excedido":
                aviso = "O saldo ultrapassaria o limite de armazenamento."
            form.add_error("quantidade", aviso)
            item.refresh_from_db()
    else:
        form = MovimentacaoForm(initial={"chave_operacao": uuid4()})
    return render(request, "estoque/detalhe.html", {
        "item": item, "form": form, "movimentacoes": item.movimentacoes.all(),
    })
