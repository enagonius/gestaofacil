from django.urls import path

from . import views

urlpatterns = [
    path("", views.painel, name="painel"),
    path("clientes/", views.clientes_lista, name="clientes_lista"),
    path("clientes/novo/", views.cliente_form, name="cliente_novo"),
    path("clientes/<int:pk>/", views.cliente_detalhe, name="cliente_detalhe"),
    path("clientes/<int:pk>/editar/", views.cliente_form, name="cliente_editar"),
    path("pedidos/", views.pedidos_lista, name="pedidos_lista"),
    path("pedidos/novo/", views.pedido_form, name="pedido_novo"),
    path("pedidos/<int:pk>/", views.pedido_detalhe, name="pedido_detalhe"),
    path("pedidos/<int:pk>/editar/", views.pedido_form, name="pedido_editar"),
    path("pedidos/<int:pk>/status/", views.pedido_status, name="pedido_status"),
]
