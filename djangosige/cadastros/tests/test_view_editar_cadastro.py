from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ..forms import EditarCadastroForm
from ..models import Cadastro
from .factories import CadastroFactory


class TestCaseBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.cadastro = CadastroFactory(
            usuario=cls.user,
            descricao="Empresa Cliente LTDA",
            tipo_pessoa=Cadastro.TipoPessoa.JURIDICA,
            cliente=True,
            fornecedor=False,
            transportadora=False,
            ativo=True,
            observacao="Observação de teste",
        )
        cls.url = cls.cadastro.get_editar_url()

    def setUp(self):
        self.client.force_login(self.user)


class TestAutenticacao(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.cadastro = CadastroFactory(usuario=cls.user)
        cls.url = cls.cadastro.get_editar_url()

    def test_usuario_nao_autenticado_e_redirecionado_para_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_usuario_autenticado_pode_acessar_pagina_para_editar_cadastro(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cadastros/editar.html")


class TestContexto(TestCaseBase):
    def test_injeta_variavel_pagina_com_valor_cadastros(self):
        response = self.client.get(self.url)
        self.assertIn("pagina", response.context)
        self.assertEqual(response.context["pagina"], "cadastros")

    def test_injeta_variavel_form_com_instancia_de_editar_cadastro_form(self):
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], EditarCadastroForm)

    def test_formulario_vem_carregado_com_dados_do_cadastro_existente(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertEqual(form.instance, self.cadastro)


class TestEditarCadastro(TestCaseBase):
    def setUp(self):
        super().setUp()
        self.dados_validos = {
            "descricao": "Empresa Cliente LTDA - Editado",
            "tipo_pessoa": Cadastro.TipoPessoa.JURIDICA,
            "cliente": True,
            "fornecedor": False,
            "transportadora": False,
            "observacao": "Observação de teste editada",
        }

    def test_editar_cadastro_com_sucesso(self):
        self.client.post(self.url, data=self.dados_validos)
        self.cadastro.refresh_from_db()
        self.assertEqual(self.cadastro.descricao, "Empresa Cliente LTDA - Editado")
        self.assertEqual(self.cadastro.observacao, "Observação de teste editada")

    def test_redireciona_para_ver_apos_editar(self):
        response = self.client.post(self.url, data=self.dados_validos)
        self.assertRedirects(response, self.cadastro.get_absolute_url())

    def test_dispara_mensagem_de_sucesso_ao_editar(self):
        response = self.client.post(self.url, data=self.dados_validos)
        mensagens = list(get_messages(response.wsgi_request))
        self.assertEqual(len(mensagens), 1)
        self.assertEqual(str(mensagens[0]), "Cadastro atualizado com sucesso!")

    def test_retorna_404_para_cadastro_inexistente(self):
        url_invalida = reverse("cadastros:editar", kwargs={"pk": 999999})
        response = self.client.get(url_invalida)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
