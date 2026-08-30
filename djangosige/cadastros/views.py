from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import CadastroFilter
from .forms import CriarCadastroForm, EditarCadastroForm, VerCadastroForm
from .models import Cadastro


class ListarCadastros(LoginRequiredMixin, FilterView):
    MAPA_RELACIONAMENTOS = {
        "clientes": {"cliente": True},
        "fornecedores": {"fornecedor": True},
        "transportadoras": {"transportadora": True},
    }
    CAMPOS_ORDENACAO_PERMITIDOS = {
        "id",
        "descricao",
        "tipo_pessoa",
        "cliente",
        "fornecedor",
        "transportadora",
    }

    template_name = "cadastros/listar.html"
    extra_context = {"pagina": "cadastros"}
    model = Cadastro
    context_object_name = "cadastros"
    paginate_by = 25
    filterset_class = CadastroFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "relacionamento" not in context:
            context["relacionamento"] = self.request.GET.get("relacionamento")

        if "order_by" not in context:
            context["order_by"] = self.request.GET.get("order_by")

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filtrar_relacionamento(queryset)

    def filtrar_relacionamento(self, queryset):
        relacionamento = self.request.GET.get("relacionamento", "").strip().lower()
        filtro = self.MAPA_RELACIONAMENTOS.get(relacionamento)

        if filtro:
            return queryset.filter(**filtro)

        return queryset

    def get_ordering(self):
        order_by = self.request.GET.get("order_by", "").strip()

        if not order_by:
            return super().get_ordering()

        campo = order_by.lstrip("-")

        if campo in self.CAMPOS_ORDENACAO_PERMITIDOS:
            return order_by

        return super().get_ordering()


class VerCadastro(LoginRequiredMixin, DetailView):
    template_name = "cadastros/ver.html"
    extra_context = {"pagina": "cadastros"}
    model = Cadastro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "form" not in context:
            context["form"] = VerCadastroForm(instance=self.object)
        return context


class CriarCadastro(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "cadastros/criar.html"
    extra_context = {"pagina": "cadastros"}
    model = Cadastro
    form_class = CriarCadastroForm
    success_message = "Cadastro criado com sucesso!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class EditarCadastro(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "cadastros/editar.html"
    extra_context = {"pagina": "cadastros"}
    model = Cadastro
    form_class = EditarCadastroForm
    success_message = "Cadastro atualizado com sucesso!"
