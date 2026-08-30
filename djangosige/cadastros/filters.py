import django_filters

from .models import Cadastro


class CadastroFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Descrição",
    )

    class Meta:
        model = Cadastro
        fields = [
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
        ]
