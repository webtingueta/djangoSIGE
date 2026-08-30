from django.test import TestCase

from ..forms import EditarCadastroForm
from ..models import Cadastro
from .factories import CadastroFactory


class TestEditarCadastroForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cadastro = CadastroFactory(tipo_pessoa=Cadastro.TipoPessoa.FISICA, descricao="Nome Antigo")

    def test_campos_presentes_no_formulario(self):
        form = EditarCadastroForm(instance=self.cadastro)
        campos_esperados = {
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
            "ativo",
            "observacao",
        }
        self.assertEqual(set(form.fields.keys()), campos_esperados)

    def test_campo_tipo_pessoa_esta_desabilitado(self):
        form = EditarCadastroForm(instance=self.cadastro)
        self.assertTrue(form.fields["tipo_pessoa"].disabled)

    def test_mantem_tipo_pessoa_original_mesmo_se_enviado_novo_valor(self):
        dados = {
            "descricao": "Nome Atualizado",
            "tipo_pessoa": Cadastro.TipoPessoa.JURIDICA,
            "cliente": True,
            "fornecedor": False,
            "transportadora": False,
            "ativo": True,
            "observacao": "",
        }
        form = EditarCadastroForm(data=dados, instance=self.cadastro)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["tipo_pessoa"], Cadastro.TipoPessoa.FISICA)

        cadastro_salvo = form.save()
        self.assertEqual(cadastro_salvo.tipo_pessoa, Cadastro.TipoPessoa.FISICA)
        self.assertEqual(cadastro_salvo.descricao, "Nome Atualizado")
