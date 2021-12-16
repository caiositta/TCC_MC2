function filterArray(inputArr){
    var found ={};
    var out = inputArr.filter(function(element){
        return found.hasOwnProperty(element)? false : (found[element]=true);
    });
    return out;
}

// GRAFICO DE LINHA RELAÇÃO DE BALANÇO
e_home = document.getElementById('lista_fechamentos')
if (e_home != null){
    var lista_geral_fechamentos = JSON.parse(document.getElementById('lista_fechamentos').value.replace(/'/g, '"'));

    lista_balancos = [];
    lista_nomes = [];
    lista_despesas = [];
    lista_faturamentos = [];

    for (var i = 0; i < lista_geral_fechamentos.length; i++) {
        lista_nomes.push(lista_geral_fechamentos[i].fechamento)
        lista_despesas.push(Math.round(lista_geral_fechamentos[i].despesas))
        lista_balancos.push(Math.round(lista_geral_fechamentos[i].balanco))
        lista_faturamentos.push(Math.round(lista_geral_fechamentos[i].faturamentos))
    };


    // GRAFICO DE LINHA RELAÇÃO DE BALANÇO
    var options = {
        series: [
            {
                name: "Balanço",
                data: lista_balancos
            },
            {
                name: "Despesas",
                data: lista_despesas
            },
            {
                name: "Faturamento",
                data: lista_faturamentos
            }
        ],
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            }
        },
        colors: ['#557ffe', '#fbabab','#9fe6cc'],
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'straight'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            categories: lista_nomes,
        },
        yaxis: {
            title: {
            text: 'Balanço'
            },
        },
    };

    var chart = new ApexCharts(document.querySelector("#fechamentos-chart"), options);
    chart.render();
}

// GRAFICO DE PIZZA TIPO DESPESAS
e_analise_desp = document.getElementById('lista_despesas')
if (e_analise_desp != null){

    var lista_despesas = JSON.parse(document.getElementById('lista_despesas').value.replace(/'/g, '"'));

    lista_tipo = [];
    // Pega os tipos
    for (var i = 0; i < lista_despesas.length; i++) {
        lista_tipo.push(lista_despesas[i].tipo)
    };
    // Tira Duplicidade dos Tipos
    lista_tipo = filterArray(lista_tipo);
    lista_principal = []

    for (var i = 0; i < lista_tipo.length; i++) {
        soma = 0
        lista_dic = [
            lista_tipo[i]
        ]

        for (var c = 0; c < lista_despesas.length; c++) {
            if (lista_despesas[c].tipo === lista_tipo[i]){
                console.log('soma:'+soma)
                soma = soma + lista_despesas[c].valor
            }
        }

        lista_dic.push(soma)
        lista_principal.push(lista_dic)
    }

    lista_valores = []
    lista_tipos = []
    for (var i = 0; i < lista_principal.length; i++) {
        lista_tipos.push(lista_principal[i][0])
        lista_valores.push(lista_principal[i][1])
    }

    // GRAFICO DE PIZZA TIPO DESPESAS
    var options = {
        series:lista_valores ,
        chart: {
        type: 'donut',
    },
    title: {
        text: 'Quantidade de Gasto das Depesas por Tipo',
        align: 'left'
    },
    labels: lista_tipos,
    responsive: [{
        breakpoint: 480,
        options: {
        chart: {
            width: 200
        },
        legend: {
            position: 'bottom'
        }
        }
    }]
    };

    var chart = new ApexCharts(document.querySelector("#tipo-chart-desp"), options);
    chart.render();
}

// GRAFICO DE PIZZA TIPO FATURAMENTOS
e_analise_fatu = document.getElementById('lista_faturamentos')
if (e_analise_fatu != null){

    var lista_faturamentos = JSON.parse(document.getElementById('lista_faturamentos').value.replace(/'/g, '"'));

    lista_tipo = [];
    // Pega os tipos
    for (var i = 0; i < lista_faturamentos.length; i++) {
        lista_tipo.push(lista_faturamentos[i].tipo)
    };
    // Tira Duplicidade dos Tipos
    lista_tipo = filterArray(lista_tipo);
    lista_principal = []

    for (var i = 0; i < lista_tipo.length; i++) {
        soma = 0
        lista_dic = [
            lista_tipo[i]
        ]

        for (var c = 0; c < lista_faturamentos.length; c++) {
            if (lista_faturamentos[c].tipo === lista_tipo[i]){
                console.log('soma:'+soma)
                soma = soma + lista_faturamentos[c].valor
            }
        }

        lista_dic.push(soma)
        lista_principal.push(lista_dic)
    }

    lista_valores = []
    lista_tipos = []
    for (var i = 0; i < lista_principal.length; i++) {
        lista_tipos.push(lista_principal[i][0])
        lista_valores.push(lista_principal[i][1])
    }

    // GRAFICO DE PIZZA TIPO FATURAMENTO
    var options = {
        series:lista_valores ,
        chart: {
        type: 'donut',
    },
    title: {
        text: 'Quantidade de Gasto das Faturamento por Tipo',
        align: 'left'
    },
    labels: lista_tipos,
    responsive: [{
        breakpoint: 480,
        options: {
        chart: {
            width: 200
        },
        legend: {
            position: 'bottom'
        }
        }
    }]
    };

    var chart = new ApexCharts(document.querySelector("#tipo-chart-fatu"), options);
    chart.render();
}
