"""URLs para o projeto DjangoSIGE"""

from django.urls import include, path

urlpatterns = [
    path("", include("djangosige.apps.base.urls")),
    path("login/", include("djangosige.apps.login.urls")),
    path("cadastro/", include("djangosige.apps.cadastro.urls")),
    path("fiscal/", include("djangosige.apps.fiscal.urls")),
    path("vendas/", include("djangosige.apps.vendas.urls")),
    path("compras/", include("djangosige.apps.compras.urls")),
    path("financeiro/", include("djangosige.apps.financeiro.urls")),
    path("estoque/", include("djangosige.apps.estoque.urls")),
]
