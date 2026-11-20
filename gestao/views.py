from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm, PedidoForm
from .models import Cliente, Pedido


@login_required
def painel(request):
    return render(request, "painel.html")


@login_required
def clientes_lista(request):
    return render(request, "clientes/lista.html", {"clientes": Cliente.objects.all()})


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
    return render(request, "pedidos/lista.html", {"pedidos": Pedido.objects.select_related("cliente")})


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
        initial = {"cliente": int(cliente)} if pedido is None and cliente.isascii() and cliente.isdigit() and len(cliente) <= 18 else {}
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
