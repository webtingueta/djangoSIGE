from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import VerCadastroForm
from .factories import CadastroFactory


class TestCaseBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.cadastro = CadastroFactory(usuario=cls.user)
        cls.url = cls.cadastro.get_absolute_url()

    def setUp(self):
        self.client.force_login(self.user)


class TestAutenticacao(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.cadastro = CadastroFactory(usuario=cls.user)
        cls.url = cls.cadastro.get_absolute_url()

    def test_usuario_nao_autenticado_e_redirecionado_para_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_usuario_autenticado_pode_acessar_a_pagina(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cadastros/ver.html")


class TestContexto(TestCaseBase):
    def test_injeta_variavel_pagina_com_valor_cadastros(self):
        response = self.client.get(self.url)
        self.assertIn("pagina", response.context)
        self.assertEqual(response.context["pagina"], "cadastros")

    def test_injeta_objeto_cadastro_no_contexto(self):
        response = self.client.get(self.url)
        self.assertIn("cadastro", response.context)
        self.assertEqual(response.context["cadastro"], self.cadastro)

    def test_injeta_form_de_visualizacao_com_instancia_correta(self):
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], VerCadastroForm)

    def test_instancia_do_form_e_o_mesmo_objeto_cadastro(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"].instance, self.cadastro)


class TestCadastroInexistente(TestCaseBase):
    def test_retorna_404_para_cadastro_inexistente(self):
        url_invalida = reverse("cadastros:ver", kwargs={"pk": 999999})
        response = self.client.get(url_invalida)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestSegurancaDetailView(TestCaseBase):
    def test_requisicao_post_rejeitada(self):
        response = self.client.post(self.cadastro.get_absolute_url(), {"descricao": "Nova Descricao Maliciosa"})
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
