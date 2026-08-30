from django import forms
from .models import Cadastro


class BaseForm(forms.ModelForm):
    class Meta:
        model = Cadastro
        fields = (
            "descricao",
            "tipo_pessoa",
            "cliente",
            "fornecedor",
            "transportadora",
            "ativo",
            "observacao",
        )


class CriarCadastroForm(BaseForm):
    class Meta(BaseForm.Meta):
        exclude = ("ativo",)


class EditarCadastroForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo_pessoa"].disabled = True

    def clean_tipo_pessoa(self):
        return self.instance.tipo_pessoa


class VerCadastroForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
