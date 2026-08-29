"""
DjangoSIGE - Sistema de Gestão Empresarial
Projeto de código aberto sobre a licença MIT.

QuerySets personalizados para filtragem de cadastros de pessoas e empresas.

Classes:
    CadastroQS: QuerySet para filtragem por tipo de pessoa, status de cliente, fornecedor, transportadora e
    status de ativo/inativo.
"""

from django.db import models


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
