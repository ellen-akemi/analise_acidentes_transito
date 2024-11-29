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
   - [https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf](#)

2. **Crie uma pasta chamada `data` na raiz do projeto** e insira os arquivos baixados nela.

   O caminho esperado pelo script para os dados é:
   ```bash
   ./data

## **Como Executar o Dashboard**

1. Após configurar o ambiente e adicionar os dados, volte para a pasta raiz do projeto:

   ```bash
   cd ..
   
4. Execute o script interface.py para iniciar o dashboard:

   ```bash
   streamlit run interface.py

5. Abra o navegador no endereço fornecido (normalmente, http://localhost:8502) para visualizar o dashboard.

   ---

## **Principais Resultados e Insights Obtidos**

Durante a análise exploratória dos dados, alguns insights e padrões interessantes foram observados:

- A maioria dos acidentes ocorre durante o período da tarde, principalmente no horário de pico por volta das 18h. No período da manhã também temos uma grande quantidade de acidentes por volta das 07h.
- A análise mostrou que a maior parte dos acidentes tem gravidade moderada a leve.
- As principais causas de acidentes incluíram reação tardia ou ineficiente do condutor, ausência de reação do condutor, acessar via sem observar outros veículos.
- Os tipos comuns de acidentes foram colisões traseiras e trasnversais e saída de leito carroçável.
- O mapa interativo revelou a concentração de acidentes em áreas.

## **Notas Importantes**

- Certifique-se de que todos os arquivos de dados necessários estão na pasta `data`.
- Caso tenha problemas ao instalar dependências, verifique a versão do Python e do Conda.

---

## **Contato**

Caso encontre problemas ou tenha dúvidas, sinta-se à vontade para entrar em contato com os desenvolvedores do projeto. 😊

---

## Pessoas Contribuidoras

[<img src="https://avatars.githubusercontent.com/u/181884443?v=4" width=115><br><sub>Ellen Akemi</sub>](https://github.com/ellen-akemi) |  [<img src="https://avatars.githubusercontent.com/u/55546267?v=4" width=115><br><sub>Priscila Miranda</sub>](https://github.com/priscilafraser) |
| :---: | :---: |

