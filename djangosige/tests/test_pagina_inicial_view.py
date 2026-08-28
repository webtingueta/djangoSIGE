from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestUsuarioNaoAutenticado(TestCase):
    def test_usuario_nao_autenticado_deve_ser_redirecionado_para_pagina_de_login(self):
        r = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(r.status_code, HTTPStatus.FOUND)
        self.assertRedirects(r, "/login/")


class TestUsuarioAutenticado(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser", password="password123")  # type: ignore

    def test_usuario_autenticado_consegue_acessar_pagina_inicial(self):
        self.client.login(username="testuser", password="password123")
        r = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(r, "base/index.html")


class TestContextoResposta(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser", password="password123")  # type: ignore

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    def test_contexto_deve_conter_data_atual_formatada(self):
        r = self.client.get(reverse("pagina_inicial"))
        self.assertIn("data_atual", r.context)
        self.assertRegex(r.context["data_atual"], r"\d{2}/\d{2}/\d{4}")

    def test_contexto_deve_conter_totais_de_cadastro(self):
        r = self.client.get(reverse("pagina_inicial"))
        self.assertIn("quantidade_cadastro", r.context)
        self.assertIsInstance(r.context["quantidade_cadastro"], dict)

    def test_contexto_deve_conter_agenda_do_dia(self):
        r = self.client.get(reverse("pagina_inicial"))
        self.assertIn("agenda_hoje", r.context)
        self.assertIsInstance(r.context["agenda_hoje"], dict)

    def test_contexto_deve_conter_alertas(self):
        r = self.client.get(reverse("pagina_inicial"))
        self.assertIn("alertas", r.context)
        self.assertIsInstance(r.context["alertas"], dict)
