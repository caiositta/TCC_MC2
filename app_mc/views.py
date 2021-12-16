from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum
from .models import Despesas, Fechamentos, Faturamentos, TipoDespesas, TipoFaturamento
from .forms import DespesasForm, FechamentosForm, FaturamentosForm, TipoDespesasForm, TipoFaturamentoForm
from django.db import connection
from datetime import datetime, date
from math import ceil
# ---PÁGINA INICIAL
@login_required
def index(request):
    # Pega a data atual
    mes_hj = date.today()
    # Pega os Fechamentos
    fechamentos = Fechamentos.objects.all()
    # Conta para organização dos cards na tela
    itens_carrosel = ceil(len(fechamentos)/3)
    # Variaveis para Estrutura da lista de cards
    lista = []
    grupo = []
    lista_grafico = []
    count = 0
    existe_mes_atual = None
    for item in fechamentos:
        # Pega as somas dos valores das Despesas e Faturamentos de suas respectivas tabelas
        despesas_bruto = Despesas.objects.filter(mes_id=item.id).aggregate(Sum('valor'))
        faturamentos_bruto = Faturamentos.objects.filter(mes_id=item.id).aggregate(Sum('valor'))

        # Tira os brutos de dentro de dicionarios e os transforma em inteiro
        despesas, faturamentos = trata_aggregate(despesas_bruto,faturamentos_bruto)
        balanco = round(faturamentos - despesas, 2)

        if item.mes.strftime('%m%Y') == mes_hj.strftime('%m%Y'):
            mes_atual = True
            existe_mes_atual = item
        else:
            mes_atual = False

        # "Pacote" de informações de cada Fechamento
        dic = {
            'fechamento':item,
            'despesas':despesas,
            'faturamentos':faturamentos,
            'balanco':balanco,
            'mes_atual':mes_atual
        }

        dic_grafico = {
            "fechamento":str(item),
            "despesas":despesas,
            "faturamentos":faturamentos,
            "balanco":balanco
        }
        lista_grafico.append(dic_grafico)
        grupo.append(dic)
        count+=1
        if len(grupo) == 3:
            lista.append(grupo)
            grupo = []
    lista.append(grupo)

    # Para monstrar o mês que irá ser criado no modal
    mes_hj_tratado = traduz_mes(mes_hj.strftime('%m'))+' / '+mes_hj.strftime('%Y')

    contas_despesas = Despesas.objects.all().values('data_vencimento','nome','mes').filter(data_pagamento__isnull=True).filter(data_vencimento__isnull=False).order_by()[:5]
    i = 0
    for item in contas_despesas:
        if item['data_vencimento'] == date.today():
            item['cor'] = 'vence_hj'
        elif item['data_vencimento'] < date.today():
            item['cor'] = 'venceu'
        else:
            item['cor'] = 'nao_venceu'
        item['data_NA'] =  item['data_vencimento'].strftime("%Y/%m/%d")
        item['data_vencimento'] = item['data_vencimento'].strftime("%d/%m/%Y")
        item['mes'] = Fechamentos.objects.filter(id=item['mes'])[0]

    return render(request, 'home.html', {
        'fechamentos':lista,
        'range':range(itens_carrosel),
        'existe_mes_atual':existe_mes_atual,
        'mes_hj':mes_hj_tratado,
        'lista_grafico':lista_grafico,
        'contas_despesas':contas_despesas
        })


# ---CRUD DESPESAS
@login_required
def criarDespesas(request,id):
    item = Fechamentos.objects.get(id=id)
    form = DespesasForm(request.POST or None,initial={'mes': item.id})
    
    if form.is_valid():
        id_return_fechamento = form.cleaned_data['mes'].id
        form.save()

        return redirect('adm_fechamentos',id=id_return_fechamento)

    return render(request,'despesas/form_despesa.html', {'form':form,'idfechamento':id})

@login_required
def atualizarDespesas(request, id):
    despesas = Despesas.objects.get(id=id)
    form = DespesasForm(request.POST or None, instance=despesas)

    if form.is_valid():
        id_return_fechamento = form.cleaned_data['mes'].id
        form.save()
        return redirect('adm_fechamentos',id=id_return_fechamento)

    return render(request, 'despesas/form_despesa.html', {'form':form,'despesas':despesas})

@login_required
def excluirDespesas(request, id):
    despesas = Despesas.objects.get(id=id)
    id_return_fechamento = Despesas.objects.get(id=id).mes_id

    if request.method == 'POST':
        despesas.delete()
        return redirect('adm_fechamentos',id=id_return_fechamento)

    return render(request, 'confirmar_remocao.html',{'parametro':despesas})
    

# ---CRUD FATURAMENTO
@login_required
def criarFaturamentos(request,id):
    item = Fechamentos.objects.get(id=id)
    form = FaturamentosForm(request.POST or None,initial={'mes': item.id})

    if form.is_valid():
        id_return_fechamento = form.cleaned_data['mes'].id
        form.save()
        return redirect('adm_fechamentos',id=id_return_fechamento)

    return render(request,'faturamentos/form_faturamento.html', {'form':form})

@login_required
def atualizarFaturamentos(request, id):
    faturamentos = Faturamentos.objects.get(id=id)
    form = FaturamentosForm(request.POST or None, instance=faturamentos)

    if form.is_valid():
        id_return_fechamento = form.cleaned_data['mes'].id
        form.save()
        return redirect('adm_fechamentos',id=id_return_fechamento)

    return render(request, 'faturamentos/form_faturamento.html', {'form':form,'faturamentos':faturamentos})

@login_required
def excluirFaturamentos(request, id):
    faturamentos = Faturamentos.objects.get(id=id)
    id_return_fechamento = Faturamentos.objects.get(id=id).mes_id

    if request.method == 'POST':
        faturamentos.delete()
        return redirect('adm_fechamentos',id=id_return_fechamento)

    return render(request, 'confirmar_remocao.html',{'parametro':faturamentos})


# ---CRUD TIPO DESPESA
@login_required
def visualizarTipoDespesas(request):
    tipo_despesa = TipoDespesas.objects.all()
    lista = []
    for item in tipo_despesa:
        qtdDespesasRegistradas = Despesas.objects.filter(tipo_id=item.id).count()
        dic = {
            'tipoDespesa':item,
            'qtd':qtdDespesasRegistradas
        }
        lista.append(dic)


    return render(request,'despesas/tabela_tipodespesas.html', {'lista':lista})

@login_required
def criarTipoDespesas(request):
    form = TipoDespesasForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_tipoDespesas')

    return render(request,'despesas/form_tipodespesas.html', {'form':form})

@login_required
def atualizarTipoDespesas(request,id):
    tipo_despesa = TipoDespesas.objects.get(id=id)
    form = TipoDespesasForm(request.POST or None, instance=tipo_despesa)

    if form.is_valid():
        form.save()
        return redirect('lista_tipoDespesas')

    return render(request, 'despesas/form_tipodespesas.html', {'form':form,'tipodespesa':tipo_despesa})

@login_required
def excluirTipoDespesas(request,id):
    tipo_despesa = TipoDespesas.objects.get(id=id)

    if request.method == 'POST':
        tipo_despesa.delete()
        return redirect('lista_tipoDespesas')

    return render(request, 'confirmar_remocao.html',{'parametro':tipo_despesa})

# ---CRUD TIPO FATURAMENTO
@login_required
def visualizarTipoFaturamentos(request):
    tipo_faturamento = TipoFaturamento.objects.all()
    lista = []
    for item in tipo_faturamento:
        qtdFaturamentosRegistradas = Faturamentos.objects.filter(tipo_id=item.id).count()
        dic = {
            'tipoFaturamento':item,
            'qtd':qtdFaturamentosRegistradas
        }
        lista.append(dic)

    return render(request,'faturamentos/tabela_tipofaturamentos.html', {'lista':lista})

@login_required
def criarTipoFaturamentos(request):
    form = TipoFaturamentoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_tipoFaturamentos')

    return render(request,'faturamentos/form_tipofaturamentos.html', {'form':form})

@login_required
def atualizarTipoFaturamentos(request,id):
    tipo_faturamento = TipoFaturamento.objects.get(id=id)
    form = TipoFaturamentoForm(request.POST or None, instance=tipo_faturamento)

    if form.is_valid():
        form.save()
        return redirect('lista_tipoFaturamentos')

    return render(request, 'faturamentos/form_tipofaturamentos.html', {'form':form,'tipofaturamento':tipo_faturamento})

@login_required
def excluirTipoFaturamentos(request,id):
    tipo_faturamento = TipoFaturamento.objects.get(id=id)

    if request.method == 'POST':
        tipo_faturamento.delete()
        return redirect('lista_tipoFaturamentos')

    return render(request, 'confirmar_remocao.html',{'parametro':tipo_faturamento})


# ---FECHAMENTO
def visualizarFechamentos(request):
    fechamentos = Fechamentos.objects.all()
    lista = []
    for item in fechamentos:
        # Pega as somas dos valores das Despesas e Faturamentos de suas respectivas tabelas
        despesas_bruto = Despesas.objects.filter(mes_id=item.id).aggregate(Sum('valor'))
        faturamentos_bruto = Faturamentos.objects.filter(mes_id=item.id).aggregate(Sum('valor'))

        # Tira os brutos de dentro de dicionarios e os transforma em inteiro
        despesas, faturamentos = trata_aggregate(despesas_bruto,faturamentos_bruto)
        balanco = round(faturamentos - despesas, 2)

        # "Pacote" de informações de cada Fechamento
        dic = {
            'fechamento':item,
            'despesas':despesas,
            'faturamentos':faturamentos,
            'balanco':balanco,
            'data_NA':item.retorna_mes().strftime("%Y/%m/%d")
        }
        lista.append(dic)

    return render(request,'fechamentos/tabela_geral_fechamento.html', {'lista':lista})

@login_required
def criarFechamentos(request):
    form = FechamentosForm(request.POST)

    if form.is_valid():
        cursor = connection.cursor()

        # Verifica se o fechamento do mês já existe
        if cursor.execute('''SELECT * FROM app_mc_fechamentos WHERE MONTH(mes) = MONTH(DATE_FORMAT(NOW(), "%Y%m%d"))''') != 0:
            erro = "Você só pode ter um fechamento mensal, e o deste mês ({}) já foi criado.".format(traduz_mes(datetime.today().strftime("%m")))
            return render(request,'fechamentos/form_fechamento.html', {'form':form,'mes_atual':traduz_mes(datetime.today().strftime("%m")),'erro':erro})
        else:
            id_mes_anterior = Fechamentos.objects.all().order_by("-id")[0]
            form.save()
            id_mes_atual = Fechamentos.objects.all().order_by("-id")[0]

            cursor.execute(f'''INSERT INTO app_mc_despesas (nome,fixo,valor,mes_id,tipo_id) SELECT nome,fixo,valor,{id_mes_atual.id} as mes_id,tipo_id FROM app_mc_despesas WHERE mes_id = {id_mes_anterior.id} AND fixo = 1''')
            cursor.execute(f'''INSERT INTO app_mc_faturamentos (nome,fixo,valor,mes_id,tipo_id) SELECT nome,fixo,valor,{id_mes_atual.id} as mes_id,tipo_id FROM app_mc_faturamentos WHERE mes_id = {id_mes_anterior.id} AND fixo = 1''')

        return redirect('home')

    return redirect('home')

@login_required
def admFechamentos(request,id):
    fechamentos = Fechamentos.objects.get(pk=id)
    despesas = Despesas.objects.filter(mes_id=id)
    faturamentos = Faturamentos.objects.filter(mes_id=id)

    return render(request,'fechamentos/tabela_fechamento.html',{
        'fechamentos':fechamentos,
        'despesas':despesas,
        'faturamentos':faturamentos,
        'idfechamento':id
        })

@login_required
def graficosFechamentos(request,id):
    fechamentos = Fechamentos.objects.filter(id=id)

    despesas = Despesas.objects.filter(mes=id)
    faturamentos = Faturamentos.objects.filter(mes=id)

    despesas_bruto = Despesas.objects.filter(mes_id=id).aggregate(Sum('valor'))
    faturamentos_bruto = Faturamentos.objects.filter(mes_id=id).aggregate(Sum('valor'))

    # Tira os brutos de dentro de dicionarios e os transforma em inteiro
    despesas_l, faturamentos_l = trata_aggregate(despesas_bruto,faturamentos_bruto)
    balanco = round(faturamentos_l - despesas_l, 2)

    
    lista_desp = []
    for item in despesas:
        dic = {
            'valor':int(item.valor),
            'tipo':str(item.tipo)
        }
        lista_desp.append(dic)

    lista_fatu = []
    for item in faturamentos:
        dic = {
            'valor':int(item.valor),
            'tipo':str(item.tipo)
        }
        lista_fatu.append(dic)

    return render(request,'fechamentos/graficos_fechamento.html',{
        'fechamentos':fechamentos,
        'lista_despesas':lista_desp,
        'lista_faturamentos':lista_fatu,
        'despesas':despesas_l,
        'faturamentos':faturamentos_l,
        'balanco':balanco
        })

# --- FUNÇÕES
# Função que traduz o mês de numero para string em portugues
def traduz_mes(num):
    lista_meses = [None,'Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    return lista_meses[int(num)]

# Função que trata o aggregate
def trata_aggregate(despesa_ag,faturamento_ag):
    # trata despesa
    if despesa_ag['valor__sum'] == None:
        despesas = 0
    else:
        despesas = float(despesa_ag['valor__sum'])
    # trata faturamento
    if faturamento_ag['valor__sum'] == None:
        faturamento = 0
    else:
        faturamento = float(faturamento_ag['valor__sum'])
    
    return despesas, faturamento
