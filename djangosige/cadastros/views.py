"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def listar_cadastros(request: HttpRequest) -> HttpResponse:
    return render(request, "cadastros/listar.html", {})


@login_required
def ver_cadastro(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, "cadastros/ver.html", {"pk": pk})


@login_required
def criar_cadastro(request: HttpRequest) -> HttpResponse:
    return render(request, "cadastros/criar.html", {})


@login_required
def editar_cadastro(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, "cadastros/editar.html", {"pk": pk})
