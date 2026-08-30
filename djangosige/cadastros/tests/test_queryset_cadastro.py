from django.test import TestCase

from ..models import Cadastro
from .factories import CadastroFactory


class TestCadastroQS(TestCase):
    @classmethod
    def setUpTestData(cls):
        CadastroFactory(
            tipo_pessoa=Cadastro.TipoPessoa.FISICA,
            ativo=True,
            cliente=True,
            fornecedor=False,
            transportadora=False,
        )
        CadastroFactory.create_batch(
            2,
            tipo_pessoa=Cadastro.TipoPessoa.JURIDICA,
            ativo=False,
            cliente=False,
            fornecedor=True,
            transportadora=False,
        )
        CadastroFactory.create_batch(
            3,
            tipo_pessoa=Cadastro.TipoPessoa.JURIDICA,
            ativo=True,
            cliente=False,
            fornecedor=False,
            transportadora=True,
        )

    def test_filtrar_tipo_pessoa(self):
        self.assertEqual(Cadastro.objects.pessoa_fisica().count(), 1)
        self.assertEqual(Cadastro.objects.pessoa_juridica().count(), 5)

    def test_filtrar_por_status_ativo(self):
        self.assertEqual(Cadastro.objects.ativos().count(), 4)
        self.assertEqual(Cadastro.objects.inativos().count(), 2)

    def test_filtrar_por_tipo_de_relacionamento(self):
        self.assertEqual(Cadastro.objects.clientes().count(), 1)
        self.assertEqual(Cadastro.objects.fornecedores().count(), 2)
        self.assertEqual(Cadastro.objects.transportadoras().count(), 3)
