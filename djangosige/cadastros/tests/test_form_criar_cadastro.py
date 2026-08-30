from django.test import TestCase

from djangosige.tests.factories import UserFactory

from ..forms import CriarCadastroForm
from ..models import Cadastro


class TestCriarCadastroForm(TestCase):
    def test_campos_presentes_no_formulario(self):
        form = CriarCadastroForm()
        campos_esperados = {
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
            "observacao",
        }
        self.assertEqual(set(form.fields.keys()), campos_esperados)
        self.assertNotIn("ativo", form.fields)

    def test_formulario_valido_com_dados_corretos(self):
        dados = {
            "descricao": "Empresa Teste LTDA",
            "tipo_pessoa": Cadastro.TipoPessoa.JURIDICA,
            "cliente": True,
            "fornecedor": False,
            "transportadora": False,
            "observacao": "Sem observações",
        }
        form = CriarCadastroForm(data=dados)
        self.assertTrue(form.is_valid())

    def test_salva_novo_cadastro_com_sucesso(self):
        dados = {
            "descricao": "Pessoa Fisica Teste",
            "tipo_pessoa": Cadastro.TipoPessoa.FISICA,
            "cliente": True,
            "fornecedor": False,
            "transportadora": False,
            "observacao": "",
        }
        form = CriarCadastroForm(data=dados)
        self.assertTrue(form.is_valid())
        cadastro = form.save(commit=False)
        cadastro.usuario = UserFactory()
        cadastro.save()

        self.assertIsNotNone(cadastro.pk)
        self.assertEqual(cadastro.descricao, "Pessoa Fisica Teste")
        self.assertTrue(cadastro.ativo)
