import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
import numpy as np


# CSS
mystyle = '''
<style>
    p {
        text-align: justify;
    }
    .css-1vq4p4l {
        padding: 1.5rem 1rem 1.5rem;
    }
    .st-ag, .st-ah {
        background-color: #245cd4 !important; 
        color: white !important; 
    }
    .st-af, .st-ag, .st-ah {
        background-color: #245cd4 !important;
        color: white !important; 
        border: none !important; 
        box-shadow: none !important; 
        border-radius: none !important;
        padding: none !important; 
    }
</style>
'''
st.markdown(mystyle, unsafe_allow_html=True)

# Carregar o DataFrame tratado
df_consolidado = pd.read_csv("df_consolidado_atualizado.csv", encoding="utf-8", sep=";")

# Nomes dos meses
meses_map = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

df_consolidado["mes_nome"] = df_consolidado["mes"].map(meses_map)
df_consolidado["semestre"] = df_consolidado["mes"].apply(lambda x: "1º Semestre" if x <= 6 else "2º Semestre")


if "df_filtrado" not in st.session_state:
    st.session_state.df_filtrado = df_consolidado.copy()

# Barra lateral com filtros e menu
with st.sidebar:
    st.title("Filtros Interativos")

    # Filtro de Ano
    anos_opcoes = ["Todos"] + list(df_consolidado["ano"].unique())
    anos_selecionados = st.multiselect(
        "Selecione os Anos", anos_opcoes, default="Todos"
    )

    # Filtro de Semestre
    semestre_selecionado = st.selectbox(
        "Selecione o Semestre", ["Todos", "1º Semestre", "2º Semestre"]
    )

    # Filtro de Mês
    meses_opcoes = ["Todos"] + list(meses_map.values())
    if semestre_selecionado != "Todos":
        meses_selecionados = []
    else:
        meses_selecionados = st.multiselect(
            "Selecione os Meses", meses_opcoes, default="Todos"
        )

    # Converter os meses para numeros
    meses_numeros = [k for k, v in meses_map.items() if v in meses_selecionados]

    # Filtrando o df
    df_temp = df_consolidado.copy()


    if "Todos" not in anos_selecionados:
        df_temp = df_temp[df_temp["ano"].isin(anos_selecionados)]

    # Priorizar o filtro de semestre
    if semestre_selecionado != "Todos":
        df_temp = df_temp[df_temp["semestre"] == semestre_selecionado]
    elif "Todos" not in meses_selecionados:
        # Aplicar filtro de meses apenas se "Todos" não estiver selecionado
        df_temp = df_temp[df_temp["mes"].isin(meses_numeros)]

    # Atualizar o DataFrame filtrado globalmente
    st.session_state.df_filtrado = df_temp

    # Menu de navegação
    choose = option_menu(
        "Visualização Análise dos dados",
        ["Distribuição de Dados", "Mapa Interativo", "Causas e Tipos", "Estatísticas Avançadas", "Período e Gravidade", "Análise Temporal", "Sobre o App"],
        icons=["bar-chart", "geo", "list", "calculator", "info-circle"],
        styles={
            "container": {"padding": "5!important", "background-color": "#F0F2F6"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#ff8585"},
            "nav-link-selected": {"background-color": "#245cd4"},
        },
    )

# Recuperarando df filtrado
df_filtrado = st.session_state.df_filtrado

# Seção "Distribuição de Dados"
if choose == "Distribuição de Dados":
    st.title("Distribuição dos Dados")

    # Histograma
    st.subheader("Histograma da Hora do Acidente")
    fig_histograma = plt.figure(figsize=(10, 6))
    sns.histplot(df_filtrado["hora"], kde=False, discrete=True, bins=24, color="cornflowerblue", edgecolor="white")
    plt.title("Distribuição da Hora do Acidente")
    plt.xlabel("Hora do Acidente")
    plt.ylabel("Quantidade de Acidentes")
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig_histograma)

    # Boxplot
    st.subheader("Boxplot da Hora do Acidente")
    fig_boxplot = plt.figure(figsize=(10, 6))
    sns.boxplot(x=df_filtrado["hora"], color="gray", width=0.4)
    plt.title("Boxplot da Hora do Acidente")
    plt.xlabel("Hora")
    st.pyplot(fig_boxplot)

    # Violin Plot
    st.subheader("Violin Plot do Total de Feridos")
    fig_violin = plt.figure(figsize=(12, 6))
    sns.violinplot(x=df_filtrado["total_feridos"], color="lightgray", inner="quart", linewidth=2)
    plt.xlim(0, 20)
    plt.xticks(range(0, 21))
    plt.title("Distribuição do Número de Feridos em Acidentes")
    plt.xlabel("Número de Feridos")
    plt.ylabel("Frequência")
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig_violin)

# Seção "Mapa Interativo"
if choose == "Mapa Interativo":
    st.title("Mapa Interativo dos Acidentes")

    # Criação do mapa
    fig_map = px.scatter_geo(
        df_filtrado,
        lat="latitude",
        lon="longitude",
        hover_name="municipio",
        size="total_feridos",
        color="gravidade_acidente",
        title="Mapa de Acidentes - Brasil",
        projection="mercator",
    )

    # Ajustando o foco no Brasil
    fig_map.update_geos(
        scope="south america",  
        center={"lat": -14.2350, "lon": -51.9253},  
        projection_scale=5,
        showland=True,
        landcolor="rgb(217, 217, 217)",
        showocean=True,
        oceancolor="rgb(204, 228, 247)",
        showcoastlines=True,
        coastlinecolor="rgb(255, 255, 255)",
    )

    fig_map.update_traces(
        marker=dict(
            line=dict(color="black", width=0.5),
        )
    )
    fig_map.update_layout(
        legend_title=dict(
            text="Gravidade do Acidente", 
            font=dict(color="black", size=14),
        ),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.8)", 
            bordercolor="black",
            borderwidth=1,
        ),
        height=800,
        width=1200,
        title_x=0.5,
    )

    st.plotly_chart(fig_map)


# Seção "Causas e Tipos"
if choose == "Causas e Tipos":
    st.title("Análise de Causas e Tipos de Acidentes")

    # Top 5 Causas
    st.subheader("Top 5 Causas Mais Comuns dos Acidentes")
    top_5_causas = df_filtrado["causa_acidente"].value_counts().head(5).reset_index()
    top_5_causas.columns = ["Causa do Acidente", "Quantidade"]
    fig_causas = px.bar(
        top_5_causas,
        x="Causa do Acidente",
        y="Quantidade",
        title="Top 5 Causas mais Comuns dos Acidentes",
        labels={"Causa do Acidente": "Causa do Acidente", "Quantidade": "Quantidade de Acidentes"},
        color="Quantidade",
        color_continuous_scale="Blues",
        text="Quantidade",
    )
    st.plotly_chart(fig_causas)

    # Top 5 Tipos
    st.subheader("Top 5 Tipos Mais Comuns de Acidentes")
    top_5_tipos = df_filtrado["tipo_acidente"].value_counts().head(5).reset_index()
    top_5_tipos.columns = ["Tipo de Acidente", "Quantidade"]
    fig_tipos = px.bar(
        top_5_tipos,
        x="Tipo de Acidente",
        y="Quantidade",
        title="Top 5 Tipos mais Comuns de Acidentes",
        labels={"Tipo de Acidente": "Tipo de Acidente", "Quantidade": "Quantidade de Acidentes"},
        color="Quantidade",
        color_continuous_scale="Viridis",
        text="Quantidade",
    )
    st.plotly_chart(fig_tipos)

# Seção "Estatísticas Avançadas"
if choose == "Estatísticas Avançadas":
    st.title("Estatísticas Avançadas")

    # Matriz de Correlação
    st.subheader("Matriz de Correlação entre Variáveis Numéricas")
    df_numerico = df_filtrado.select_dtypes(include=["number"])
    correlation_matrix = df_numerico.corr()
    fig_corr = plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Matriz de Correlação")
    st.pyplot(fig_corr)

    # Relação entre Vítimas e Clima
    st.subheader("Relação entre Número de Vítimas e Condições Meteorológicas")
    fig_vitimas_clima = px.scatter(
        df_filtrado,
        x="total_feridos",
        y="condicao_metereologica",
        color="gravidade_acidente",
        title="Relação entre Número de Vítimas e Condições Meteorológicas",
        labels={
            "total_feridos": "Número de Vítimas",
            "condicao_metereologica": "Condição Meteorológica",
        },
        hover_data=["municipio", "hora"],
        color_continuous_scale="YlOrRd",
    )
    st.plotly_chart(fig_vitimas_clima)


# Seção "Sobre o App"
if choose == "Sobre o App":
    st.title("Sobre o App")
    st.write(
        """
        Este dashboard foi desenvolvido para explorar e visualizar dados de acidentes de trânsito no Brasil.
        Utilize as seções do menu para navegar por filtros, análises estatísticas e gráficos interativos.
        """
    )

if choose == "Período e Gravidade":
    st.title("Análises por Período do Dia e Gravidade")

    # Análise por Período do Dia
    st.subheader("Número de Acidentes por Período do Dia")
    periodos_dia_selecionados = st.selectbox(
        "Selecione o Período do Dia",
        ["Todas as Opções"] + list(df_consolidado["periodo_dia"].unique()),
        index=0,
    )

    if periodos_dia_selecionados != "Todas as Opções":
        df_filtrado_periodo = df_filtrado[df_filtrado["periodo_dia"] == periodos_dia_selecionados]
    else:
        df_filtrado_periodo = df_filtrado

    acidentes_por_periodo_dia = df_filtrado_periodo.groupby("periodo_dia").size().reset_index(name="quantidade_acidentes")
    fig_periodo = plt.figure(figsize=(10, 6))
    sns.barplot(x="quantidade_acidentes", y="periodo_dia", data=acidentes_por_periodo_dia, palette="magma")
    plt.title(f"Número de Acidentes por Período do Dia ({periodos_dia_selecionados})", fontsize=16, fontweight="bold")
    plt.xlabel("Quantidade de Acidentes", fontsize=14)
    plt.ylabel("Período do Dia", fontsize=14)

    for index, value in enumerate(acidentes_por_periodo_dia["quantidade_acidentes"]):
        plt.text(value + 2, index, str(value), color="black", ha="left", va="center", fontsize=12)

    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_periodo)

    # Análise por Gravidade
    st.subheader("Número de Acidentes por Gravidade")
    gravidades_selecionadas = st.selectbox(
        "Selecione a Gravidade do Acidente",
        ["Todas as Opções"] + list(df_consolidado["gravidade_acidente"].unique()),
        index=0,
    )

    if gravidades_selecionadas != "Todas as Opções":
        df_filtrado_gravidade = df_filtrado[df_filtrado["gravidade_acidente"] == gravidades_selecionadas]
    else:
        df_filtrado_gravidade = df_filtrado

    acidentes_por_gravidade = df_filtrado_gravidade.groupby("gravidade_acidente").size().reset_index(name="quantidade_acidentes")
    fig_gravidade = plt.figure(figsize=(10, 6))
    sns.barplot(x="quantidade_acidentes", y="gravidade_acidente", data=acidentes_por_gravidade, palette="YlOrRd")
    plt.title(f"Número de Acidentes por Gravidade ({gravidades_selecionadas})", fontsize=16, fontweight="bold")
    plt.xlabel("Quantidade de Acidentes", fontsize=14)
    plt.ylabel("Gravidade do Acidente", fontsize=14)

    for index, value in enumerate(acidentes_por_gravidade["quantidade_acidentes"]):
        plt.text(value + 3, index, str(value), color="black", ha="left", va="center", fontsize=12)

    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_gravidade)


# Seção "Análise Temporal"
if choose == "Análise Temporal":
    st.title("Análise Temporal de Acidentes")

    # Gráfico de Acidentes por Mês
    st.subheader("Número de Acidentes por Mês")
    acidentes_por_mes = df_filtrado.groupby("mes").size().reset_index(name="quantidade_acidentes")
    fig_mes = plt.figure(figsize=(10, 6))
    sns.barplot(x="mes", y="quantidade_acidentes", data=acidentes_por_mes, palette="Blues_d")
    plt.title("Número de Acidentes por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Quantidade de Acidentes")
    plt.xticks(ticks=np.arange(12), labels=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig_mes)

    # Gráfico de Linha para Acidentes Fatais por Mês
    acidentes_fatais = df_filtrado[df_filtrado["gravidade_acidente"] == "Grave"]
    acidentes_fatais_por_mes = acidentes_fatais.groupby("mes").size().reset_index(name="quantidade_acidentes_fatais")

    st.subheader("Evolução de Acidentes Fatais por Mês")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="mes", y="quantidade_acidentes_fatais", data=acidentes_fatais_por_mes, marker="o", color="red", ax=ax)
    ax.set_title("Evolução de Acidentes Fatais por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Quantidade de Acidentes Fatais")
    ax.set_xticks(range(12))
    ax.set_xticklabels(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])
    ax.grid(True)
    st.pyplot(fig)

    # Gráfico de Acidentes Fatais por Ano
    acidentes_fatais_por_ano = acidentes_fatais.groupby("ano").size().reset_index(name="quantidade_acidentes_fatais")

    st.subheader("Número de Acidentes Fatais por Ano")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="ano", y="quantidade_acidentes_fatais", data=acidentes_fatais_por_ano, palette="Reds", ax=ax)
    ax.set_title("Número de Acidentes Fatais por Ano", fontsize=16, fontweight="bold", color="darkred")
    ax.set_xlabel("Ano", fontsize=12, fontweight="bold")
    ax.set_ylabel("Quantidade de Acidentes Fatais", fontsize=12, fontweight="bold")
    ax.grid(True, axis="y", linestyle="--", alpha=0.7)

    # Anotações nos Gráficos
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.0f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=10,
            color="black",
            fontweight="bold",
            xytext=(0, 5),
            textcoords="offset points",
        )

    st.pyplot(fig)
