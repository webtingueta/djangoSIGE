"""
DjangoSIGE - Sistema de Gestão Empresarial.
Projeto de código aberto sob a licença MIT.
"""

from django.urls import include, path

from . import views as v

urlpatterns = [
    path("", v.pagina_inicial, name="pagina_inicial"),
    path("login/", include("djangosige.apps.login.urls")),
    path("cadastro/", include("djangosige.apps.cadastro.urls")),
    path("fiscal/", include("djangosige.apps.fiscal.urls")),
    path("vendas/", include("djangosige.apps.vendas.urls")),
    path("compras/", include("djangosige.apps.compras.urls")),
    path("financeiro/", include("djangosige.apps.financeiro.urls")),
    path("estoque/", include("djangosige.apps.estoque.urls")),
]
