import pandas as pd

# Carregar arquivos
df_2021 = pd.read_csv("2021.csv", encoding="iso-8859-1", sep=";")
df_2022 = pd.read_csv("2022.csv", encoding="utf-8", sep=",")
df_2023 = pd.read_csv("2023.csv", encoding="iso-8859-1", sep=";")
df_2024 = pd.read_csv("2024.csv", encoding="utf-8", sep=",")

print(df_2021.head())
print(df_2022.head())
print(df_2023.head())
print(df_2024.head())

# Concatenar DataFrames em um único conjunto de dados
df_consolidado = pd.concat([df_2021, df_2022, df_2023, df_2024], ignore_index=True)
print(df_consolidado.head())

# Salvar DataFrame consolidado em um novo arquivo CSV
df_consolidado.to_csv("consolidado.csv", index=False, encoding="utf-8", sep=";")
print("Arquivo consolidado salvo como 'consolidado.csv'.")

# Validação e limpeza dos dados

# Verificando existência de valores nulos (ausentes)
print(df_consolidado.isnull().sum())

# Obs.: temos 4 colunas com valores ausentes: classificacao_acidente, regional, delegacia e uop.
print("\nTemos 4 colunas com valores ausentes")

# Tratamento
for column in df_consolidado.columns:
    if df_consolidado[column].dtype == "object":  
        moda = df_consolidado[column].mode()[0] 
        df_consolidado[column].fillna(moda, inplace=True)
    else:  
        media = df_consolidado[column].mean() 
        df_consolidado[column].fillna(media, inplace=True)

print("\nValores ausentes por coluna após o tratamento:")
print(df_consolidado.isnull().sum())

# Verificar tipo de dados das colunas
df_consolidado.info()

# Alterando para o formato datatime
df_consolidado["data_inversa"] = pd.to_datetime(df_consolidado["data_inversa"], errors="coerce")
df_consolidado["hora"] = pd.to_datetime(df_consolidado["horario"], format="%H:%M:%S").dt.hour
df_consolidado.info()

# Verificar duplicatas
print(f"\nNúmero de duplicatas: {df_consolidado.duplicated().sum()}")
# Obs.: veja que não possui duplicatas, nesse caso, não precisamos remover
print("\nNão temos duplicatas")

# Alterando outros formatos de colunas
df_consolidado["br"] = df_consolidado["br"].astype(object)
df_consolidado.info()

# Verificar datas incoerentes
print(df_consolidado[df_consolidado["data_inversa"] > pd.Timestamp.today()])  # Datas futuras

# Salvar novo arquivo consolidado tratado
df_consolidado.to_csv("consolidado_tratado.csv", index=False, encoding="utf-8", sep=";")
print("Arquivo consolidado tratado salvo como 'consolidado_tratado.csv'.")

# Engenharia de Atributos

# Extração de informações de data
# Já temos uma coluna para o dia da semana, vamos extrair o dia, mês e o ano
df_consolidado["dia"] = df_consolidado["data_inversa"].dt.day # Dia
df_consolidado["mes"] = df_consolidado["data_inversa"].dt.month  # Mês 
df_consolidado["ano"] = df_consolidado["data_inversa"].dt.year  # Ano

# Nova coluna para o período do dia
def periodo_dia(hour):
    if 6 <= hour < 12:
        return "Manhã"
    elif 12 <= hour < 18:
        return "Tarde"
    elif 18 <= hour < 24:
        return "Noite"
    else:
        return "Madrugada"

df_consolidado["periodo_dia"] = df_consolidado["hora"].apply(periodo_dia)

# Nova coluna para o total de feridos
df_consolidado["total_feridos"] = df_consolidado["feridos_leves"] + df_consolidado["feridos_graves"]

# Nova coluna para gravidade do acidente
def gravidade_acidente(row):
    if row["classificacao_acidente"] == "Com Vítimas Fatais":
        return "Grave"
    elif row["classificacao_acidente"] == "Com Vítimas Feridas":
        return "Moderado"
    else:
        return "Leve"

df_consolidado["gravidade_acidente"] = df_consolidado.apply(gravidade_acidente, axis=1)

# Coluna com faixas para o número total de feridos
faixas_feridos = [0, 3, 10, float('inf')]
rótulos_feridos = ["Poucos", "Moderado", "Grave"]
df_consolidado["faixa_feridos"] = pd.cut(df_consolidado["feridos"], bins=faixas_feridos, labels=rótulos_feridos, right=False)

print(df_consolidado[["feridos", "faixa_feridos"]].head())

# Verificando resumo do DataFrame com as novas colunas
print("\n Resumo das 10 primeiras linhas do DataFrame com as novas colunas:")
print(df_consolidado.head(10))

# Agrupamento para análise

# Agrupar por tipo de acidente e gravidade do acidente
tipo_gravidade = df_consolidado.groupby(["tipo_acidente", "gravidade_acidente"]).size().reset_index(name="contagem")
print(tipo_gravidade)

# Contagem de acidentes por região (uf)
acidentes_por_uf = df_consolidado.groupby("uf").size().reset_index(name="quantidade_acidentes")
print(acidentes_por_uf)

# Contagem de acidentes por condição meteorológica
acidentes_por_clima = df_consolidado.groupby("condicao_metereologica").size().reset_index(name="quantidade_acidentes")
print(acidentes_por_clima)

# Contagem de acidentes por gravidade do acidente
acidentes_por_gravidade = df_consolidado.groupby("gravidade_acidente").size().reset_index(name="quantidade_acidentes")
print(acidentes_por_gravidade)

# Contagem de acidentes por período do dia
acidentes_por_periodo_dia = df_consolidado.groupby("periodo_dia").size().reset_index(name="quantidade_acidentes")
print(acidentes_por_periodo_dia)
