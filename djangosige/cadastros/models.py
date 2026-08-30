"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.

Modelos para cadastros de pessoas e empresas.

Modelos:
    Cadastro: Modelo para cadastros de pessoas e empresas.
"""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from djangosige.models import TimeStampedModel


class CadastroQS(models.QuerySet):
    """
    QuerySet para filtragem por tipo de pessoa, status de cliente, fornecedor, transportadora e
    status de ativo/inativo.

    Métodos:
        pessoa_fisica(): Retorna cadastros de pessoas físicas.
        pessoa_juridica(): Retorna cadastros de pessoas jurídicas.
        clientes(): Retorna cadastros que são clientes.
        fornecedores(): Retorna cadastros que são fornecedores.
        transportadoras(): Retorna cadastros que são transportadoras.
        ativos(): Retorna cadastros que estão ativos.
        inativos(): Retorna cadastros que estão inativos.
    """

    def pessoa_fisica(self):
        """Retorna cadastros de pessoas físicas."""
        return self.filter(tipo_pessoa="F")

    def pessoa_juridica(self):
        """Retorna cadastros de pessoas jurídicas."""
        return self.filter(tipo_pessoa="J")

    def clientes(self):
        """Retorna cadastros que são clientes."""
        return self.filter(cliente=True)

    def fornecedores(self):
        """Retorna cadastros que são fornecedores."""
        return self.filter(fornecedor=True)

    def transportadoras(self):
        """Retorna cadastros que são transportadoras."""
        return self.filter(transportadora=True)

    def ativos(self):
        """Retorna cadastros que estão ativos."""
        return self.filter(ativo=True)

    def inativos(self):
        """Retorna cadastros que estão inativos."""
        return self.filter(ativo=False)


class CadastroManager(models.Manager):
    """Gerenciador de modelo para cadastros de pessoas e empresas."""


class Cadastro(TimeStampedModel):
    """
    Modelo para cadastros de pessoas e empresas.

    Atributos:
        usuario (ForeignKey): O usuário que registrou este cadastro.
        descricao (CharField): Uma descrição para o cadastro. Nome ou Razão Social.
        tipo_pessoa (CharField): O tipo de pessoa para este cadastro (Física ou Jurídica).
        cliente (BooleanField): Indica se este cadastro é um cliente.
        fornecedor (BooleanField): Indica se este cadastro é um fornecedor.
        transportadora (BooleanField): Indica se este cadastro é uma transportadora.
        ativo (BooleanField): Indica se este cadastro está ativo.
        observacao (TextField): Observações adicionais sobre este cadastro.

    Metodos:
        __str__(): Retorna a descrição do cadastro.
        get_absolute_url(): Retorna a URL absoluta para visualizar o cadastro.
    """

    class TipoPessoa(models.TextChoices):
        FISICA = "F", _("Pessoa Física")
        JURIDICA = "J", _("Pessoa Jurídica")

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("usuário"),
        help_text=_("O usuário que registrou este cadastro."),
    )

    descricao = models.CharField(
        _("descrição"),
        max_length=255,
        unique=True,
        help_text=_("Uma descrição para o cadastro. Nome ou Razão Social."),
    )

    tipo_pessoa = models.CharField(
        _("tipo de pessoa"),
        max_length=1,
        choices=TipoPessoa.choices,
        default=TipoPessoa.FISICA,
        help_text=_("O tipo de pessoa para este cadastro."),
    )

    cliente = models.BooleanField(
        _("cliente"),
        default=False,
        help_text=_("Indica se este cadastro é um cliente."),
    )

    fornecedor = models.BooleanField(
        _("fornecedor"),
        default=False,
        help_text=_("Indica se este cadastro é um fornecedor."),
    )

    transportadora = models.BooleanField(
        _("transportadora"),
        default=False,
        help_text=_("Indica se este cadastro é uma transportadora."),
    )

    ativo = models.BooleanField(
        _("ativo"),
        default=True,
        help_text=_("Indica se este cadastro está ativo."),
    )

    observacao = models.TextField(
        _("observação"),
        blank=True,
        help_text=_("Observações adicionais sobre este cadastro."),
    )

    objects = CadastroManager.from_queryset(CadastroQS)()

    class Meta:
        ordering = ("descricao",)
        verbose_name = _("cadastro")
        verbose_name_plural = _("cadastros")

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return reverse("cadastros:ver", kwargs={"pk": self.pk})

    def get_editar_url(self):
        return reverse("cadastros:editar", kwargs={"pk": self.pk})
