"""
DjangoSIGE - Sistema de Gestão Empresarial.
Projeto de código aberto sob a licença MIT.
"""

from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .services import DashboardService


class PaginaInicialView(LoginRequiredMixin, TemplateView):
    template_name: str = "base/index.html"

    def get_context_data(self, **kwargs):
        service = DashboardService()

        metricas = service.metricas()
        movimento_dia, saldo = service.movimento_caixa()

        kwargs.update(
            {
                "data_atual": service.hoje.strftime("%d/%m/%Y"),
                "quantidade_cadastro": metricas["totais_cadastro"],
                "agenda_hoje": metricas["agenda_hoje"],
                "alertas": metricas["alertas"],
                "movimento_dia": movimento_dia,
            }
        )

        if saldo is not None:
            kwargs["saldo"] = saldo

        return kwargs


pagina_inicial = PaginaInicialView.as_view()


class Handler404View(TemplateView):
    template_name: str = "404.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, status=HTTPStatus.NOT_FOUND)


handler404 = Handler404View.as_view()


class Handler500View(TemplateView):
    template_name: str = "500.html"

    def get(self, request: HttpRequest, exception: Exception, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, status=HTTPStatus.INTERNAL_SERVER_ERROR)


handler500 = Handler500View.as_view()
