"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.

Admin para cadastros de pessoas e empresas.

Classes:
    CadastroAdmin: Classe de administração para o modelo Cadastro, permitindo a visualização e gerenciamento de
    cadastros de pessoas e empresas no painel de administração do Django.
"""

from django.contrib import admin

from .models import Cadastro


@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Cadastro, permitindo a visualização e gerenciamento de cadastros de pessoas
    e empresas no painel de administração do Django.
    """

    list_display = (
        "descricao",
        "tipo_pessoa",
        "cliente",
        "fornecedor",
        "transportadora",
        "ativo",
    )
    list_filter = ("tipo_pessoa", "cliente", "fornecedor", "transportadora", "ativo")
    search_fields = ("descricao",)
