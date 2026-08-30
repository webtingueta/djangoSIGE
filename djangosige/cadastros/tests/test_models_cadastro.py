from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from ..models import Cadastro
from .factories import CadastroFactory


class TestCriarCadastro(TestCase):
    def test_criar_cadastro_com_sucesso(self):
        self.assertEqual(Cadastro.objects.count(), 0)

        cadastro = CadastroFactory(
            descricao="Empresa ABC",
            tipo_pessoa=Cadastro.TipoPessoa.JURIDICA,
            cliente=True,
            fornecedor=True,
            transportadora=False,
            ativo=True,
            observacao="Observações do cadastro",
        )
        self.assertEqual(Cadastro.objects.count(), 1)
        self.assertEqual(cadastro.descricao, "Empresa ABC")

    def test_descricao_unica(self):
        CadastroFactory(descricao="Empresa Duplicada")

        with self.assertRaises(IntegrityError):
            CadastroFactory(descricao="Empresa Duplicada")


class TestMetodos(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cadastro = CadastroFactory(descricao="Empresa XYZ")

    def test_str(self):
        self.assertEqual(str(self.cadastro), "Empresa XYZ")

    def test_get_absolute_url(self):
        self.assertEqual(self.cadastro.get_absolute_url(), reverse("cadastros:ver", kwargs={"pk": self.cadastro.pk}))

    def test_get_editar_url(self):
        self.assertEqual(self.cadastro.get_editar_url(), reverse("cadastros:editar", kwargs={"pk": self.cadastro.pk}))
