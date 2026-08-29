"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def listar_cadastros(request):
    template_name = "cadastros/listar.html"
    context = {"pagina": "cadastros"}
    return render(request, template_name, context)


@login_required
def ver_cadastro(request, pk):
    template_name = "cadastros/ver.html"
    context = {"pagina": "cadastros", "pk": pk}
    return render(request, template_name, context)


@login_required
def criar_cadastro(request):
    template_name = "cadastros/criar.html"
    context = {"pagina": "cadastros"}
    return render(request, template_name, context)


@login_required
def editar_cadastro(request, pk):
    template_name = "cadastros/editar.html"
    context = {"pagina": "cadastros", "pk": pk}
    return render(request, template_name, context)
