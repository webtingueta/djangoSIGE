from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import EditarCadastroForm
from ..models import Cadastro


class TestEditarCadastroForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser")

        cls.cadastro = Cadastro.objects.create(
            descricao="Empresa Teste",
            usuario=cls.user,
            tipo_pessoa=Cadastro.TipoPessoa.FISICA,
            cliente=True,
            fornecedor=False,
            transportadora=False,
            observacao="Observação de teste",
        )

    def test_form_valid(self):
        form = EditarCadastroForm(
            instance=self.cadastro,
            data={
                "descricao": "Empresa Teste Atualizada",
                "tipo_pessoa": Cadastro.TipoPessoa.FISICA,
                "cliente": True,
                "fornecedor": False,
                "transportadora": False,
                "ativo": True,
                "observacao": "Observação atualizada",
            },
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = EditarCadastroForm(
            instance=self.cadastro,
            data={
                "descricao": "",
                "tipo_pessoa": "",
                "cliente": True,
                "fornecedor": False,
                "transportadora": False,
                "ativo": True,
                "observacao": "",
            },
        )
        self.assertFalse(form.is_valid())
