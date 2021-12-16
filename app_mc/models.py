from django.db import models

def traduz_mes(num):
    lista_meses = [None,'Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    return lista_meses[int(num)]

class TipoDespesas(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nome


class TipoFaturamento(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nome

class Despesas(models.Model):
    nome = models.CharField(max_length=245)
    mes = models.ForeignKey("Fechamentos", on_delete=models.CASCADE, related_name='fechamentoDespesas')
    data_vencimento = models.DateField(null=True,blank=True)
    data_pagamento = models.DateField(null=True,blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    fixo = models.BooleanField(help_text="Marque caso seja uma despesa que você tenha todo mês.")
    tipo = models.ForeignKey("TipoDespesas", on_delete=models.CASCADE, related_name='tipoDespesa',null=True,blank=True)

    def __str__(self):
        return self.nome

    def datav_barra(self):
        if self.data_vencimento != None:
            return self.data_vencimento.strftime("%d/%m/%Y")

    def datap_barra(self):
        if self.data_pagamento != None:
            return self.data_pagamento.strftime("%d/%m/%Y")

class Faturamentos(models.Model):
    nome = models.CharField(max_length=255)
    mes = models.ForeignKey("Fechamentos", on_delete=models.CASCADE, related_name='fechamentoFaturamentos')
    data_vencimento = models.DateField(null=True,blank=True)
    data_pagamento = models.DateField(null=True,blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    fixo = models.BooleanField(help_text="Marque caso seja um faturamento que você tenha todo mês.")
    tipo = models.ForeignKey("TipoFaturamento", on_delete=models.CASCADE, related_name='tipoFaturamento',null=True,blank=True)

    def __str__(self):
        return self.nome

    def datav_barra(self):
        if self.data_vencimento != None:
            return self.data_vencimento.strftime("%d/%m/%Y")

    def datap_barra(self):
        if self.data_pagamento != None:
            return self.data_pagamento.strftime("%d/%m/%Y")

class Fechamentos(models.Model):
    mes = models.DateField(auto_now_add=True, unique_for_month=True)

    def __str__(self):
        mes = traduz_mes(self.mes.strftime("%m"))
        ano = self.mes.strftime("%Y")
        mes_ano = str(mes)+' / '+str(ano)
        return str(mes_ano)

    def retorna_mes(self):
        return self.mes
