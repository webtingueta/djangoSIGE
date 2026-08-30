from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .factories import CadastroFactory


class TestCaseBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.url = reverse("cadastros:listar")

    def setUp(self):
        self.client.force_login(self.user)


class TestAutenticacao(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="usuario_teste", password="senha_teste")
        cls.url = reverse("cadastros:listar")

    def test_usuario_sem_autenticacao_nao_pode_acessar_a_pagina(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('cadastros:listar')}")

    def test_usuario_autenticado_pode_acessar_a_pagina(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cadastros/listar.html")


class TestContexto(TestCaseBase):
    def test_injeta_variavel_pagina_com_valor_cadastros(self):
        response = self.client.get(self.url)
        self.assertIn("pagina", response.context)
        self.assertEqual(response.context["pagina"], "cadastros")

    def test_injeta_variavel_relacionamento_sem_valor(self):
        response = self.client.get(self.url)
        self.assertIn("relacionamento", response.context)
        self.assertFalse(response.context["relacionamento"])

    def test_injeta_variavel_relacionamento_com_valor(self):
        response = self.client.get(self.url, {"relacionamento": "clientes"})
        self.assertIn("relacionamento", response.context)
        self.assertEqual(response.context["relacionamento"], "clientes")

    def test_injeta_variavel_order_by_sem_valor(self):
        response = self.client.get(self.url)
        self.assertIn("order_by", response.context)
        self.assertFalse(response.context["order_by"])

    def test_injeta_variavel_order_by_com_valor(self):
        response = self.client.get(self.url, {"order_by": "descricao"})
        self.assertIn("order_by", response.context)
        self.assertEqual(response.context["order_by"], "descricao")


class TestListagemVazia(TestCaseBase):
    def test_listagem_vazia(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["cadastros"]), 0)


class TestListagemComCadastros(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        CadastroFactory.create_batch(1, cliente=True, fornecedor=False, transportadora=False)
        CadastroFactory.create_batch(2, cliente=False, fornecedor=True, transportadora=False)
        CadastroFactory.create_batch(3, cliente=False, fornecedor=False, transportadora=True)

    def test_listagem_com_cadastros(self):
        response = self.client.get(self.url)
        self.assertIn("cadastros", response.context)
        self.assertEqual(len(response.context["cadastros"]), 6)

    def test_listagem_com_filtro_de_relacionamento(self):
        cenarios = [("clientes", 1), ("fornecedores", 2), ("transportadoras", 3)]
        for relacionamento, quantidade in cenarios:
            with self.subTest(relacionamento=relacionamento):
                response = self.client.get(self.url, {"relacionamento": relacionamento})
                self.assertEqual(len(response.context["cadastros"]), quantidade)

    def test_relacionamento_invalido_retorna_todos_os_registros(self):
        response = self.client.get(self.url, {"relacionamento": "invalido"})
        self.assertEqual(len(response.context["cadastros"]), 6)


class TestPaginacao(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        CadastroFactory.create_batch(30)

    def test_maximo_de_cadastros_por_pagina(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["cadastros"]), 25)

    def test_listagem_com_paginacao_segunda_pagina(self):
        response = self.client.get(self.url, {"page": 2})
        self.assertEqual(len(response.context["cadastros"]), 5)


class TestOrdenacao(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.cadastro_a = CadastroFactory(descricao="AAAA")
        cls.cadastro_z = CadastroFactory(descricao="ZZZZ")

    def test_ordena_por_campo_permitido_ascendente_e_descendente(self):
        response_asc = self.client.get(self.url, {"order_by": "descricao"})
        cadastros_asc = list(response_asc.context["cadastros"])
        self.assertEqual(cadastros_asc[0], self.cadastro_a)

        response_desc = self.client.get(self.url, {"order_by": "-descricao"})
        cadastros_desc = list(response_desc.context["cadastros"])
        self.assertEqual(cadastros_desc[0], self.cadastro_z)

    def test_ignora_campo_de_ordenacao_invalido(self):
        response = self.client.get(self.url, {"order_by": "campo_inexistente"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
