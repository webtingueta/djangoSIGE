from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ..forms import CriarCadastroForm
from ..models import Cadastro


class TestCaseBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.url = reverse("cadastros:criar")

    def setUp(self):
        self.client.force_login(self.user)


class TestAutenticacao(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.url = reverse("cadastros:criar")

    def test_usuario_nao_autenticado_e_redirecionado_para_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_usuario_autenticado_pode_acessar_pagina_criacao(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cadastros/criar.html")


class TestContexto(TestCaseBase):
    def test_injeta_variavel_pagina_com_valor_cadastros(self):
        response = self.client.get(self.url)
        self.assertIn("pagina", response.context)
        self.assertEqual(response.context["pagina"], "cadastros")

    def test_injeta_variavel_form_com_instancia_de_CriarCadastroForm(self):
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CriarCadastroForm)


class TestCriarCadastro(TestCaseBase):
    def setUp(self):
        super().setUp()
        self.dados_validos = {
            "descricao": "Empresa Cliente LTDA",
            "tipo_pessoa": Cadastro.TipoPessoa.JURIDICA,
            "cliente": True,
            "fornecedor": False,
            "transportadora": False,
            "observacao": "Observação de teste",
        }

    def test_criar_cadastro_com_sucesso(self):
        self.client.post(self.url, data=self.dados_validos)
        self.assertTrue(Cadastro.objects.filter(descricao="Empresa Cliente LTDA").exists())

    def test_redireciona_para_pagina_de_detalhes_apos_criar_cadastro(self):
        response = self.client.post(self.url, data=self.dados_validos)
        cadastro = Cadastro.objects.get(descricao="Empresa Cliente LTDA")
        self.assertEqual(response.url, cadastro.get_absolute_url())

    def test_cadastro_associa_usuario_logado(self):
        self.client.post(self.url, data=self.dados_validos)
        cadastro = Cadastro.objects.get(descricao="Empresa Cliente LTDA")
        self.assertEqual(cadastro.usuario, self.user)

    def test_dispara_mensagem_de_sucesso_ao_criar(self):
        response = self.client.post(self.url, data=self.dados_validos)
        mensagens = list(get_messages(response.wsgi_request))
        self.assertEqual(len(mensagens), 1)
        self.assertEqual(str(mensagens[0]), "Cadastro criado com sucesso!")
