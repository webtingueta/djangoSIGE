from django.urls import path

from . import views

app_name = "cadastros"

urlpatterns = [
    path("", views.listar_cadastros, name="listar"),
    path("ver/<int:pk>/", views.ver_cadastro, name="ver"),
    path("editar/<int:pk>/", views.editar_cadastro, name="editar"),
    path("criar/", views.criar_cadastro, name="criar"),
]
