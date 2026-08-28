"""
DjangoSIGE - Sistema de Gestão Empresarial.
Projeto de código aberto sob a licença MIT.

Context processor para a versão do DjangoSIGE.
"""

from djangosige.version import __VERSION__


def sige_version(request):
    """Adiciona a versão do DjangoSIGE ao contexto do template."""
    return {"versao": __VERSION__}
