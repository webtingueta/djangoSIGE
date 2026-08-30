from django.urls import path

from . import views

app_name = "cadastros"

urlpatterns = [
    path("", views.ListarCadastros.as_view(), name="listar"),
    path("criar/", views.CriarCadastro.as_view(), name="criar"),
    path("<int:pk>/", views.VerCadastro.as_view(), name="ver"),
    path("<int:pk>/editar/", views.EditarCadastro.as_view(), name="editar"),
]
