from django import forms
from . import models

# Formulario para cadastrar um Tipo de Despesa
class TipoDespesasForm(forms.ModelForm):
    class Meta:
        model = models.TipoDespesas
        fields = [
            'nome'
        ]

# Formulario para cadastrar um Tipo de Faturamento
class TipoFaturamentoForm(forms.ModelForm):
    class Meta:
        model = models.TipoFaturamento
        fields = [
            'nome'
        ]

# Formulário para cadastrar uma Despesa
class DespesasForm(forms.ModelForm):
    class Meta:
        model = models.Despesas
        fields = [
            'nome',
            'mes',
            'data_vencimento',
            'data_pagamento',
            'valor',
            'fixo',
            'tipo'
        ]
        widgets = {
            'mes': forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_vencimento'].widget.attrs.update({'class':'mask-data'})
        self.fields['data_pagamento'].widget.attrs.update({'class':'mask-data'})
        self.fields['valor'].widget.attrs.update({'class':'mask-money'})


# Formulario para cadastrar um Faturamento
class FaturamentosForm(forms.ModelForm):
    class Meta:
        model = models.Faturamentos
        fields = [
            'nome',
            'mes',
            'data_vencimento',
            'data_pagamento',
            'valor',
            'fixo',
            'tipo'
        ]
        widgets = {
            'mes': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_vencimento'].widget.attrs.update({'class':'mask-data'})
        self.fields['data_pagamento'].widget.attrs.update({'class':'mask-data'})
        self.fields['valor'].widget.attrs.update({'class':'mask-money'})

# Formulario para cadastrar um Fechamento
class FechamentosForm(forms.ModelForm):
    class Meta:
        model = models.Fechamentos
        exclude = [
        ]
        widgets = {
        }


