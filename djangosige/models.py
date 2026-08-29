"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.

Modelos base para o DjangoSIGE.

Classes:
    TimeStampedModel: Uma classe abstrata base que prove campos auto-atualizáveis ``criado`` e ``modificado``.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Uma classe abstrata base que prove campos auto-atualizáveis ``criado`` e ``modificado``.

    Atributos:
        criado (DateTimeField): O campo de data e hora em que o objeto foi criado.
        modificado (DateTimeField): O campo de data e hora em que o objeto foi modificado pela última vez.
    """

    criado = models.DateTimeField(
        _("criado"),
        auto_now_add=True,
        help_text=_("A hora em que o objeto foi criado."),
    )
    modificado = models.DateTimeField(
        _("modificado"),
        auto_now=True,
        help_text=_("A hora em que o objeto foi modificado pela última vez."),
    )

    class Meta:
        abstract = True
