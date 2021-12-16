from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),

    # Despesas
    path('criar/despesas/<int:id>', views.criarDespesas, name="criar_despesas"),
    path('atualizar/despesas/<int:id>/', views.atualizarDespesas, name="atualizar_despesas"),
    path('excluir/despesas/<int:id>/', views.excluirDespesas, name="excluir_despesas"),

    # Tipo de Despesas
    path('tipoDespesas', views.visualizarTipoDespesas, name="lista_tipoDespesas"),
    path('criar/tipoDespesas', views.criarTipoDespesas, name="criar_tipoDespesas"),
    path('atualizar/tipoDespesas/<int:id>/', views.atualizarTipoDespesas, name="atualizar_tipoDespesas"),
    path('excluir/tipoDespesas/<int:id>/', views.excluirTipoDespesas, name="excluir_tipoDespesas"),

    # Faturamentos
    path('criar/faturamentos/<int:id>', views.criarFaturamentos, name="criar_faturamentos"),
    path('atualizar/faturamentos/<int:id>/', views.atualizarFaturamentos, name="atualizar_faturamentos"),
    path('excluir/faturamentos/<int:id>/', views.excluirFaturamentos, name="excluir_faturamentos"),

    # Tipo de Faturamentos
    path('tipoFaturamentos', views.visualizarTipoFaturamentos, name="lista_tipoFaturamentos"),
    path('criar/tipoFaturamentos', views.criarTipoFaturamentos, name="criar_tipoFaturamentos"),
    path('atualizar/tipoFaturamentos/<int:id>/', views.atualizarTipoFaturamentos, name="atualizar_tipoFaturamentos"),
    path('excluir/tipoFaturamentos/<int:id>/', views.excluirTipoFaturamentos, name="excluir_tipoFaturamentos"),

    # Fechamentos
    path('fechamentos', views.visualizarFechamentos, name="lista_fechamentos"),
    path('atualizar/fechamentos/<int:id>/', views.admFechamentos, name="adm_fechamentos"),
    path('administrar/fechamentos/<int:id>', views.admFechamentos, name="adm_fechamentos"),
    path('analisar/fechamentos/<int:id>', views.graficosFechamentos, name="graficosFechamentos"),
    path('criar/fechamentos', views.criarFechamentos, name="criar_fechamentos"),


]
