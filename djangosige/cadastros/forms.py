"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.

Formulários para cadastros de pessoas e empresas.

Formularios:
    CriarCadastroForm: Formulário para criar um novo cadastro.
    EditarCadastroForm: Formulário para atualizar um cadastro.
    VerCadastroForm: Formulário para visualizar os dados de um cadastro.
"""

from django import forms

from .models import Cadastro


class CriarCadastroForm(forms.ModelForm):
    """
    Formulário para criar um novo cadastro.

    Campos:
        descricao (CharField): Uma descrição para o cadastro. Nome ou Razão Social.
        tipo_pessoa (ChoiceField): O tipo de pessoa para este cadastro (Física ou Jurídica).
        cliente (BooleanField): Indica se este cadastro é um cliente.
        fornecedor (BooleanField): Indica se este cadastro é um fornecedor.
        transportadora (BooleanField): Indica se este cadastro é uma transportadora.
        observacao (CharField): Observações adicionais sobre este cadastro.

    Meta:
        model: O modelo associado a este formulário, que é o modelo Cadastro.
        fields: Os campos do modelo que serão incluídos no formulário.
    """

    class Meta:
        model = Cadastro
        fields = (
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
            "observacao",
        )


class EditarCadastroForm(forms.ModelForm):
    """
    Formulário para atualizar um cadastro.

    Campos:
        descricao (CharField): Uma descrição para o cadastro. Nome ou Razão Social.
        tipo_pessoa (ChoiceField): O tipo de pessoa para este cadastro (Física ou Jurídica).
        cliente (BooleanField): Indica se este cadastro é um cliente.
        fornecedor (BooleanField): Indica se este cadastro é um fornecedor.
        transportadora (BooleanField): Indica se este cadastro é uma transportadora.
        ativo (BooleanField): Indica se este cadastro está ativo.
        observacao (CharField): Observações adicionais sobre este cadastro.

    Meta:
        model: O modelo associado a este formulário, que é o modelo Cadastro.
        fields: Os campos do modelo que serão incluídos no formulário.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo_pessoa"].disabled = True

    class Meta:
        model = Cadastro
        fields = (
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
            "ativo",
            "observacao",
        )


class VerCadastroForm(forms.ModelForm):
    """
    Formulário para visualizar os dados de um cadastro.

    Campos:
        descricao (CharField): Uma descrição para o cadastro. Nome ou Razão Social.
        tipo_pessoa (ChoiceField): O tipo de pessoa para este cadastro (Física ou Jurídica).
        cliente (BooleanField): Indica se este cadastro é um cliente.
        fornecedor (BooleanField): Indica se este cadastro é um fornecedor.
        transportadora (BooleanField): Indica se este cadastro é uma transportadora.
        ativo (BooleanField): Indica se este cadastro está ativo.
        observacao (CharField): Observações adicionais sobre este cadastro.

    Meta:
        model: O modelo associado a este formulário, que é o modelo Cadastro.
        fields: Os campos do modelo que serão incluídos no formulário.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True

    class Meta:
        model = Cadastro
        fields = (
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
            "ativo",
            "observacao",
        )
