# **Projeto de Análise e Visualização de Dados de Acidentes**

Este projeto é um dashboard interativo para explorar e visualizar dados relacionados a acidentes de trânsito.

---

## **Como Configurar o Ambiente**

Siga os passos abaixo para configurar o ambiente virtual e executar o projeto:

1. **Crie e ative um ambiente virtual:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_REPOSITORIO>
   
2. **Crie e ative um ambiente virtual:**

   - **Navegue até a pasta `configure_env`:**
     ```bash
     cd configure_env
     ```

   - Crie o ambiente com o arquivo `environment.yml`:
     ```bash
     conda env create -f environment.yml
     ```

   - Instale os pacotes necessários com o arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Ative o ambiente criado:**

   ```bash
   conda activate <NOME_DO_AMBIENTE>

## **Como Configurar os Dados**

1. **Baixe os dados necessários** no seguinte link:
   - [Link para os Dados](#)

2. **Crie uma pasta chamada `data` na raiz do projeto** e insira os arquivos baixados nela.

   O caminho esperado pelo script para os dados é:
   ```bash
   ./data

## **Como Executar o Dashboard**

1. Após configurar o ambiente e adicionar os dados, volte para a pasta raiz do projeto:

   ```bash
   cd ..
   
2. Execute o script interface.py para iniciar o dashboard:
   ```bash
   streamlit run interface.py

3. Abra o navegador no endereço fornecido (normalmente, http://localhost:8501) para visualizar o dashboard.

