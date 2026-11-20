from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm
from .models import Cliente


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
    return render(request, "clientes/detalhe.html", {"cliente": cliente})
