import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import numpy as np

# Carregar o DataFrame tratado
df_consolidado = pd.read_csv("df_consolidado_atualizado.csv", encoding="utf-8", sep=";")

# Sidebar para filtros (para mês e ano)
st.sidebar.title("Filtros Interativos")
anos_selecionados = st.sidebar.multiselect("Selecione os Anos", df_consolidado["ano"].unique(), default=df_consolidado["ano"].unique())
meses_selecionados = st.sidebar.multiselect("Selecione os Meses", df_consolidado["mes"].unique(), default=df_consolidado["mes"].unique())

# Filtrando os dados com base nas seleções da sidebar
df_filtrado = df_consolidado[
    (df_consolidado["ano"].isin(anos_selecionados)) &
    (df_consolidado["mes"].isin(meses_selecionados))
]

# Título
st.title("Análise Exploratória de Acidentes de Trânsito")

# --------------------------------------------------------
# Seção 1: Distribuição dos Dados
st.header("Distribuição dos Dados")

# Histogramas e Boxplots
st.subheader("Histograma da Hora do Acidente")
fig_histograma = plt.figure(figsize=(10, 6))
sns.histplot(df_filtrado["hora"], kde=False, discrete=True, bins=24, color="cornflowerblue", edgecolor="white", linewidth=1.2)
plt.title("Distribuição da Hora do Acidente")
plt.xlabel("Hora do Acidente")
plt.ylabel("Quantidade de Acidentes")
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_histograma)

st.subheader("Boxplot da Hora do Acidente")
fig_boxplot = plt.figure(figsize=(10, 6))
sns.boxplot(x=df_filtrado["hora"], color="gray", width=0.4)
plt.title("Boxplot da Hora do Acidente")
plt.xlabel("Hora")
st.pyplot(fig_boxplot)

# Violin Plot do Total de Feridos
st.subheader("Violin Plot do Total de Feridos")
fig_violin = plt.figure(figsize=(12, 6))
sns.violinplot(x=df_filtrado['total_feridos'], color='lightgray', inner='quart', linewidth=2)
plt.xlim(0, 20)
plt.xticks(range(0, 21))
plt.title("Distribuição do Número de Feridos em Acidentes")
plt.xlabel("Número de Feridos")
plt.ylabel("Frequência")
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_violin)

# Matriz de Correlação
st.subheader("Matriz de Correlação entre Variáveis Numéricas")
df_numerico = df_filtrado.select_dtypes(include=["number"])
correlation_matrix = df_numerico.corr()
fig_corr = plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Matriz de Correlação das Variáveis Numéricas")
st.pyplot(fig_corr)

# --------------------------------------------------------
# Seção 2: Gráficos de Causas e Tipos de Acidentes
st.header("Análises de Causas e Tipos de Acidentes")

# Top 5 Causas
st.subheader("Top 5 Causas Mais Comuns dos Acidentes")
top_5_causas = df_filtrado["causa_acidente"].value_counts().head(5).reset_index()
top_5_causas.columns = ["Causa do Acidente", "Quantidade"]
fig_causas = px.bar(top_5_causas, 
                    x="Causa do Acidente", 
                    y="Quantidade", 
                    title="Top 5 Causas mais Comuns dos Acidentes",
                    labels={"Causa do Acidente": "Causa do Acidente", "Quantidade": "Quantidade de Acidentes"},
                    color="Quantidade", 
                    color_continuous_scale="Blues", 
                    text="Quantidade")
fig_causas.update_traces(texttemplate='%{text}', textposition='outside', 
                         marker=dict(line=dict(color='black', width=1))) 
st.plotly_chart(fig_causas)

# Top 5 Tipos
st.subheader("Top 5 Tipos Mais Comuns de Acidentes")
top_5_tipos = df_filtrado["tipo_acidente"].value_counts().head(5).reset_index()
top_5_tipos.columns = ["Tipo de Acidente", "Quantidade"]
fig_tipos = px.bar(top_5_tipos, 
                   x="Tipo de Acidente", 
                   y="Quantidade", 
                   title="Top 5 Tipos mais Comuns de Acidentes",
                   labels={"Tipo de Acidente": "Tipo de Acidente", "Quantidade": "Quantidade de Acidentes"},
                   color="Quantidade", 
                   color_continuous_scale="Viridis", 
                   text="Quantidade")
fig_tipos.update_traces(texttemplate='%{text}', textposition='outside', 
                        marker=dict(line=dict(color='black', width=1)))  
st.plotly_chart(fig_tipos)

# --------------------------------------------------------
# Seção 3: Número de Acidentes por Período do Dia
st.header("Análise de Acidentes por Período do Dia")

# Filtro de Período do Dia (incluindo "Todas as Opções")
periodos_dia_selecionados = st.selectbox(
    "Selecione o Período do Dia", 
    ["Todas as Opções"] + list(df_consolidado["periodo_dia"].unique()), 
    index=0
)

# Filtrando os dados por período do dia selecionado
if periodos_dia_selecionados != "Todas as Opções":
    df_filtrado_periodo = df_filtrado[df_filtrado["periodo_dia"] == periodos_dia_selecionados]
else:
    df_filtrado_periodo = df_filtrado

# Número de Acidentes por Período do Dia
acidentes_por_periodo_dia = df_filtrado_periodo.groupby("periodo_dia").size().reset_index(name="quantidade_acidentes")
fig_periodo = plt.figure(figsize=(10, 6))
sns.barplot(x="quantidade_acidentes", y="periodo_dia", data=acidentes_por_periodo_dia, palette="magma")
plt.title(f"Número de Acidentes por Período do Dia ({periodos_dia_selecionados})", fontsize=16, fontweight='bold')
plt.xlabel("Quantidade de Acidentes", fontsize=14)
plt.ylabel("Período do Dia", fontsize=14)

for index, value in enumerate(acidentes_por_periodo_dia["quantidade_acidentes"]):
    plt.text(value + 2, index, str(value), color="black", ha="left", va="center", fontsize=12)

plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout() 
st.pyplot(fig_periodo)

# --------------------------------------------------------
# Seção 4: Número de Acidentes por Gravidade
st.header("Análise de Acidentes por Gravidade")

# Filtro de Gravidade do Acidente (incluindo "Todas as Opções")
gravidades_selecionadas = st.selectbox(
    "Selecione a Gravidade do Acidente", 
    ["Todas as Opções"] + list(df_consolidado["gravidade_acidente"].unique()), 
    index=0
)

# Filtrando os dados por gravidade selecionada
if gravidades_selecionadas != "Todas as Opções":
    df_filtrado_gravidade = df_filtrado[df_filtrado["gravidade_acidente"] == gravidades_selecionadas]
else:
    df_filtrado_gravidade = df_filtrado

# Número de Acidentes por Gravidade
acidentes_por_gravidade = df_filtrado_gravidade.groupby("gravidade_acidente").size().reset_index(name="quantidade_acidentes")
fig_gravidade = plt.figure(figsize=(10, 6))
sns.barplot(x="quantidade_acidentes", y="gravidade_acidente", data=acidentes_por_gravidade, palette="YlOrRd")
plt.title(f"Número de Acidentes por Gravidade ({gravidades_selecionadas})", fontsize=16, fontweight='bold')
plt.xlabel("Quantidade de Acidentes", fontsize=14)
plt.ylabel("Gravidade do Acidente", fontsize=14)

for index, value in enumerate(acidentes_por_gravidade["quantidade_acidentes"]):
    plt.text(value + 3, index, str(value), color="black", ha="left", va="center", fontsize=12)

plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(fig_gravidade)

# --------------------------------------------------------
# Seção 5: Mapa Interativo
st.header("Distribuição Geográfica dos Acidentes")

st.subheader("Mapa Interativo dos Acidentes")
fig_map = px.scatter_geo(df_filtrado, 
                         lat="latitude", 
                         lon="longitude", 
                         hover_name="municipio", 
                         size="total_feridos",  
                         color="gravidade_acidente", 
                         title="Distribuição Geográfica dos Acidentes - Brasil",
                         color_discrete_map={"Leve": "green", "Grave": "orange", "Fatal": "red"},
                         opacity=0.6,  
                         projection="mercator",  
                         template="plotly_dark", 
                         size_max=30,  
                         hover_data=["municipio", "total_feridos", "gravidade_acidente", "hora"])  
fig_map.update_geos(
    scope="south america", 
    center={"lat": -14.2350, "lon": -51.9253}, 
    projection_scale=8,  
    showland=True,  
    landcolor="lightgray",  
    showcoastlines=True,  
    coastlinecolor="white", 
    coastlinewidth=1,  
    showocean=True,  
    oceancolor="black", 
)
fig_map.update_layout(
    height=600,  
    width=1000,  
    showlegend=True,  
    legend_title="Gravidade do Acidente", 
    title_x=0.5,  
    title_y=0.98,  
    title_font=dict(size=24, color='white'),  
    geo=dict(visible=True, showframe=False, projection_type="mercator")
)
st.plotly_chart(fig_map)

# --------------------------------------------------------
# Seção 6: Relação entre Vítimas e Condições Meteorológicas
st.header("Relação entre Número de Vítimas e Condições Meteorológicas")

st.subheader("Gráfico de Dispersão entre Vítimas e Condições Meteorológicas")
fig_vitimas_clima = px.scatter(df_filtrado, 
                                x="total_feridos", 
                                y="condicao_metereologica", 
                                color="gravidade_acidente", 
                                title="Relação entre Número de Vítimas e Condições Meteorológicas",
                                labels={"total_feridos": "Número de Vítimas", 
                                        "condicao_metereologica": "Condição Meteorológica"},
                                hover_data=["municipio", "hora"],
                                color_continuous_scale="YlOrRd")
st.plotly_chart(fig_vitimas_clima)

# --------------------------------------------------------
# Seção 7: Análise Temporal 
st.header("Análise Temporal de Acidentes")

# Gráfico de Acidentes por Mês
st.subheader("Número de Acidentes por Mês")
acidentes_por_mes = df_filtrado.groupby("mes").size().reset_index(name="quantidade_acidentes")
fig_mes = plt.figure(figsize=(10, 6))
sns.barplot(x="mes", y="quantidade_acidentes", data=acidentes_por_mes, palette="Blues_d")
plt.title("Número de Acidentes por Mês")
plt.xlabel("Mês")
plt.ylabel("Quantidade de Acidentes")
plt.xticks(ticks=np.arange(12), labels=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_mes)

# Gráfico de Linha para Acidentes Fatais
acidentes_fatais = df_filtrado[df_filtrado["gravidade_acidente"] == "Grave"]

# Contagem de acidentes fatais por mês
acidentes_fatais_por_mes = acidentes_fatais.groupby("mes").size().reset_index(name="quantidade_acidentes_fatais")

# Gráfico de linhas para acidentes fatais por mês
st.subheader("Evolução de Acidentes Fatais por Mês")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x="mes", y="quantidade_acidentes_fatais", data=acidentes_fatais_por_mes, marker='o', color='red', ax=ax)
ax.set_title("Evolução de Acidentes Fatais por Mês")
ax.set_xlabel("Mês")
ax.set_ylabel("Quantidade de Acidentes Fatais")
ax.set_xticks(range(12))
ax.set_xticklabels(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])
ax.grid(True)
st.pyplot(fig)

# Contagem de acidentes fatais por ano
acidentes_fatais_por_ano = acidentes_fatais.groupby("ano").size().reset_index(name="quantidade_acidentes_fatais")

# Gráfico de barras para acidentes fatais por ano
st.subheader("Número de Acidentes Fatais por Ano")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="ano", y="quantidade_acidentes_fatais", data=acidentes_fatais_por_ano, palette="Reds", ax=ax)
ax.set_title("Número de Acidentes Fatais por Ano", fontsize=16, fontweight='bold', color='darkred')
ax.set_xlabel("Ano", fontsize=12, fontweight='bold')
ax.set_ylabel("Quantidade de Acidentes Fatais", fontsize=12, fontweight='bold')
ax.grid(True, axis="y", linestyle="--", alpha=0.7)

# Anotação nos gráficos de barras
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                fontsize=10, color='black', fontweight='bold', 
                xytext=(0, 5), textcoords='offset points')

st.pyplot(fig)