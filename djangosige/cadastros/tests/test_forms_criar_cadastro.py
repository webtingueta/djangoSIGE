from django.test import TestCase

from ..forms import CriarCadastroForm
from ..models import Cadastro


class TestCriarCadastroForm(TestCase):
    def test_form_valid(self):
        form = CriarCadastroForm(
            data={
                "descricao": "Empresa Teste",
                "tipo_pessoa": Cadastro.TipoPessoa.FISICA,
                "cliente": True,
                "fornecedor": False,
                "transportadora": False,
                "observacao": "Observação de teste",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = CriarCadastroForm(
            data={
                "descricao": "",
                "tipo_pessoa": "",
                "cliente": True,
                "fornecedor": False,
                "transportadora": False,
                "observacao": "",
            }
        )
        self.assertFalse(form.is_valid())
