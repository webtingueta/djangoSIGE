from django.test import TestCase

from ..forms import VerCadastroForm
from .factories import CadastroFactory


class TestVerCadastroForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cadastro = CadastroFactory()

    def test_todos_os_campos_estao_desabilitados(self):
        form = VerCadastroForm(instance=self.cadastro)

        for name, field in form.fields.items():
            with self.subTest(campo=name):
                self.assertTrue(
                    field.disabled,
                    f"O campo '{name}' no VerCadastroForm deveria ter disabled=True",
                )

    def test_carrega_dados_corretos_da_instancia(self):
        form = VerCadastroForm(instance=self.cadastro)
        self.assertEqual(form.instance, self.cadastro)
        self.assertEqual(form.initial["descricao"], self.cadastro.descricao)
