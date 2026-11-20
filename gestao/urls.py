from django.urls import path

from . import views

urlpatterns = [
    path("", views.painel, name="painel"),
    path("clientes/", views.clientes_lista, name="clientes_lista"),
    path("clientes/novo/", views.cliente_form, name="cliente_novo"),
    path("clientes/<int:pk>/", views.cliente_detalhe, name="cliente_detalhe"),
    path("clientes/<int:pk>/editar/", views.cliente_form, name="cliente_editar"),
]
