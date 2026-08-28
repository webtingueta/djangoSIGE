from typing import ClassVar

from django.db.models import Count, F, Q
from django.utils import timezone

from djangosige.apps.cadastro.models import Cliente, Empresa, Fornecedor, Produto, Transportadora
from djangosige.apps.compras.models import OrcamentoCompra, PedidoCompra
from djangosige.apps.financeiro.models import Entrada, MovimentoCaixa, Saida
from djangosige.apps.vendas.models import OrcamentoVenda, PedidoVenda


class DashboardService:
    STATUS_PENDENTE = "0"
    STATUS_CONTAS_ABERTAS: ClassVar[tuple[str, ...]] = ("1", "2")

    def __init__(self, data_referencia=None):
        self.hoje = data_referencia or timezone.localdate()

    def metricas(self) -> dict:
        """Retorna as métricas do dashboard, incluindo totais de cadastro, agenda e alertas."""

        agenda_vendas, alertas_vendas = self.__metricas_vendas()
        agenda_compras, alertas_compras = self.__metricas_compras()
        agenda_fin, alertas_fin = self.__metricas_financeiro()

        return {
            "totais_cadastro": self.__totais_cadastro(),
            "agenda_hoje": {**agenda_vendas, **agenda_compras, **agenda_fin},
            "alertas": {
                "produtos_baixo_estoque": self.__produtos_baixo_estoque(),
                **alertas_vendas,
                **alertas_compras,
                **alertas_fin,
            },
        }

    def movimento_caixa(self) -> tuple:
        """Retorna o movimento do caixa do dia e o saldo final do último movimento anterior, se houver."""

        movimento_dia = MovimentoCaixa.objects.filter(data_movimento=self.hoje).first()

        if movimento_dia:
            return movimento_dia, None

        ultimo = MovimentoCaixa.objects.filter(data_movimento__lt=self.hoje).order_by("-data_movimento").first()

        return None, (ultimo.saldo_final if ultimo else "0,00")

    def __totais_cadastro(self) -> dict:
        """Retorna os totais de cadastro de clientes, fornecedores, produtos, empresas e transportadoras."""

        return {
            "clientes": Cliente.objects.count(),
            "fornecedores": Fornecedor.objects.count(),
            "produtos": Produto.objects.count(),
            "empresas": Empresa.objects.count(),
            "transportadoras": Transportadora.objects.count(),
        }

    def __produtos_baixo_estoque(self) -> int:
        """Retorna a quantidade de produtos com estoque atual menor ou igual ao estoque mínimo."""

        return Produto.objects.filter(estoque_atual__lte=F("estoque_minimo")).count()

    def __agregar_hoje_e_atrasados(self, model, campo_data: str, statuses: list) -> dict:
        """Agrega a quantidade de registros do modelo fornecido com base no campo de data e nos status fornecidos.
        Retorna um dicionário com as chaves 'hoje' e 'atrasados', representando a quantidade de registros para hoje e a
        quantidade de registros atrasados, respectivamente."""

        filtro_base = Q(**{f"{campo_data}__isnull": False}, status__in=statuses)

        return model.objects.aggregate(
            hoje=Count("id", filter=filtro_base & Q(**{campo_data: self.hoje})),
            atrasados=Count("id", filter=filtro_base & Q(**{f"{campo_data}__lte": self.hoje})),
        )

    def __metricas_vendas(self) -> tuple[dict, dict]:
        orc = self.__agregar_hoje_e_atrasados(OrcamentoVenda, "data_vencimento", [self.STATUS_PENDENTE])
        ped = self.__agregar_hoje_e_atrasados(PedidoVenda, "data_entrega", [self.STATUS_PENDENTE])

        agenda = {
            "orcamento_venda_hoje": orc["hoje"],
            "pedido_venda_hoje": ped["hoje"],
        }
        alertas = {
            "orcamentos_venda_vencidos": orc["atrasados"],
            "pedidos_venda_atrasados": ped["atrasados"],
        }
        return agenda, alertas

    def __metricas_compras(self) -> tuple[dict, dict]:
        orc = self.__agregar_hoje_e_atrasados(OrcamentoCompra, "data_vencimento", [self.STATUS_PENDENTE])
        ped = self.__agregar_hoje_e_atrasados(PedidoCompra, "data_entrega", [self.STATUS_PENDENTE])

        agenda = {
            "orcamento_compra_hoje": orc["hoje"],
            "pedido_compra_hoje": ped["hoje"],
        }
        alertas = {
            "orcamentos_compra_vencidos": orc["atrasados"],
            "pedidos_compra_atrasados": ped["atrasados"],
        }
        return agenda, alertas

    def __metricas_financeiro(self) -> tuple[dict, dict]:
        rec = self.__agregar_hoje_e_atrasados(Entrada, "data_vencimento", self.STATUS_CONTAS_ABERTAS)
        pag = self.__agregar_hoje_e_atrasados(Saida, "data_vencimento", self.STATUS_CONTAS_ABERTAS)

        agenda = {
            "contas_receber_hoje": rec["hoje"],
            "contas_pagar_hoje": pag["hoje"],
        }
        alertas = {
            "contas_receber_atrasadas": rec["atrasados"],
            "contas_pagar_atrasadas": pag["atrasados"],
        }
        return agenda, alertas
