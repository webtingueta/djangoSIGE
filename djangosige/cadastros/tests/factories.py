import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from djangosige.tests.factories import UserFactory

from ..models import Cadastro


class CadastroFactory(DjangoModelFactory):
    class Meta:
        model = Cadastro

    usuario = factory.SubFactory(UserFactory)
    descricao = fuzzy.FuzzyText(length=50)
    tipo_pessoa = fuzzy.FuzzyChoice([Cadastro.TipoPessoa.FISICA, Cadastro.TipoPessoa.JURIDICA])
    cliente = fuzzy.FuzzyChoice([True, False])
    fornecedor = fuzzy.FuzzyChoice([True, False])
    transportadora = fuzzy.FuzzyChoice([True, False])
    ativo = True
    observacao = ""
