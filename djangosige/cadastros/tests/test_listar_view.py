from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAcessoNaoAutenticado(TestCase):
    def test_usuario_sem_autenticacao_nao_pode_acessar_a_pagina(self):
        response = self.client.get(reverse("cadastros:listar"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('cadastros:listar')}")


class TestAcessoAutenticado(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")

    def setUp(self):
        self.client.login(username="usuario_teste", password="senha_teste")

    def test_usuario_autenticado_pode_acessar_a_pagina(self):
        response = self.client.get(reverse("cadastros:listar"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cadastros/listar.html")

    def test_keyword_pagina_no_contexto_da_resposta(self):
        response = self.client.get(reverse("cadastros:listar"))
        self.assertIn("pagina", response.context)
        self.assertEqual(response.context["pagina"], "cadastros")
