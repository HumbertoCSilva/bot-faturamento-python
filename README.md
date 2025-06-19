# Bot de Consulta de Faturamento para Telegram

## 📄 Descrição

Este é um bot para Telegram desenvolvido em Python que serve como uma interface inteligente para consultar dados de faturamento diário a partir de uma planilha Excel. O bot foi projetado para entender tanto datas específicas quanto consultas em linguagem natural para feriados nacionais brasileiros, tornando a obtenção de dados rápida e intuitiva.

O projeto é um exemplo completo de um ciclo de desenvolvimento, desde a leitura e processamento de dados com `pandas`, passando pela criação de um bot interativo com `python-telegram-bot`, até o gerenciamento seguro de chaves de API com variáveis de ambiente.

## ✨ Funcionalidades

- **Consulta por Data Específica:** Retorna os dados de faturamento ao receber uma data no formato `DD/MM/AAAA`.
- **Consulta por Feriados:** Entende nomes de feriados nacionais (ex: "natal 2023", "tiradentes 2024") e calcula a data correta para a busca.
- **Consulta por Períodos:** Reconhece períodos (ex: "semana do carnaval 2024") e retorna um resumo agregado e os dados detalhados.
- **Processamento de Linguagem Natural:** Utiliza um sistema de mapeamento de palavras-chave e normalização de texto (removendo acentos e ignorando maiúsculas/minúsculas) para entender as solicitações de forma flexível.
- **Gerenciamento Seguro de Segredos:** Utiliza o padrão da indústria de variáveis de ambiente (`.env` para desenvolvimento local) para o token da API, garantindo que informações sensíveis não sejam expostas no código-fonte.

## 📂 Estrutura do Projeto

A estrutura de arquivos do projeto está organizada da seguinte forma:

bot_faturamento_python/
│
├── venv/                   # Pasta do ambiente virtual isolado do Python
├── .env                    # Arquivo de configuração local (NÃO É ENVIADO AO GIT)
├── .gitignore              # Arquivo que define o que o Git deve ignorar
├── Faturamento.xlsx        # Planilha com os dados de faturamento (Exemplo de nome)
├── bot.py                  # O código-fonte principal da aplicação
└── requirements.txt        # Lista de todas as dependências do projeto

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas Principais:**
    - `python-telegram-bot`: Framework para interagir com a API do Telegram.
    - `pandas`: Para leitura, manipulação e análise dos dados da planilha Excel.
    - `openpyxl` & `xlrd`: Motores utilizados pelo pandas para ler diferentes formatos de arquivos Excel.
    - `holidays`: Para calcular com precisão as datas de feriados nacionais brasileiros.
    - `python-dotenv`: Para carregar variáveis de ambiente de um arquivo `.env` localmente.

## 🚀 Instalação e Configuração

Siga estes passos para configurar e executar o projeto localmente.

### 1. Pré-requisitos
- [Python](https://www.python.org/downloads/) (versão 3.9 ou superior)
- [Git](https://git-scm.com/downloads/) (opcional, para controle de versão)

### 2. Passos de Instalação
Clone ou baixe os arquivos para uma pasta local. Abra um terminal nessa pasta e siga os comandos:

```sh
# Criar o ambiente virtual (só precisa ser feito uma vez)
python -m venv venv

# Ativar o ambiente virtual (precisa ser feito toda vez que for trabalhar no projeto)
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Instalar todas as dependências necessárias
pip install -r requirements.txt

3. Arquivos de Configuração
Planilha de Dados:

Coloque seu arquivo Excel na pasta raiz do projeto.
Abra o arquivo bot.py e ajuste a variável NOME_ARQUIVO_EXCEL para corresponder exatamente ao nome do seu arquivo.
Verifique também se o nome na variável NOME_COLUNA_DATA corresponde ao cabeçalho da coluna de datas na sua planilha.
Token do Bot:

Crie um arquivo chamado .env na pasta raiz do projeto.
Dentro deste arquivo, adicione a seguinte linha, substituindo pelo seu token real obtido com o @BotFather:

TELEGRAM_TOKEN="SEU_TOKEN_AQUI"

▶️ Executando o Bot
Com o ambiente virtual ativo ((venv)) e os arquivos configurados, inicie o bot com o seguinte comando no terminal:

python bot.py

O terminal exibirá a mensagem >>> Bot inteligente iniciado com sucesso! <<<. Para parar o bot, pressione Ctrl+C.

🤖 Como Usar o Bot
Abra uma conversa com seu bot no Telegram e envie uma mensagem.

Exemplos de Comandos:

31/12/2024
natal 2023
proclamação da república 2024
semana do carnaval 2023
📐 Arquitetura do Código
O script bot.py é dividido em seções lógicas:

Configurações Globais: Define constantes como nomes de arquivos, colunas e o MAPEAMENTO_EVENTOS, que funciona como um dicionário para "traduzir" as solicitações do usuário para nomes de feriados oficiais.
Funções de Manipulação de Dados:
carregar_dados(): Responsável por ler o arquivo Excel com o pandas na inicialização do bot e armazenar os dados em memória para acesso rápido.
buscar_faturamento_por_data() e buscar_faturamento_por_periodo(): Funções otimizadas para consultar os dados em memória a partir de uma data ou intervalo.
normalizar_texto(): Uma função utilitária que remove acentos e converte o texto para minúsculas, permitindo uma comparação de texto flexível.
processar_evento_texto(): O cérebro da interpretação de linguagem natural. Ele usa o MAPEAMENTO_EVENTOS e a biblioteca holidays para converter um texto como "natal 2023" em uma data concreta.
Lógica do Bot (Handlers):
start(): Responde ao comando /start com uma mensagem de boas-vindas.
message_handler(): O handler principal que recebe todo o texto do usuário. Ele primeiro tenta interpretar a mensagem como uma data DD/MM/AAAA. Se falhar, ele assume que é um evento e chama a processar_evento_texto() para obter o resultado.
main(): A função principal que inicializa o bot, carrega os dados e começa a "escutar" por mensagens no Telegram.
❓ Troubleshooting / Problemas Comuns
Erro FileNotFoundError: Verifique se o nome do arquivo Excel na variável NOME_ARQUIVO_EXCEL no código bot.py é exatamente igual ao nome do arquivo na pasta.
Bot não inicia ou dá erro de Token: Verifique se o arquivo .env existe, se o nome da variável é TELEGRAM_TOKEN, e se o valor é o token correto e válido do @BotFather.
Comandos não funcionam: Certifique-se de que o ambiente virtual (venv) está ativo no terminal onde você executou python bot.py.
Feriado não reconhecido: Verifique se a palavra-chave para o feriado desejado existe no dicionário MAPEAMENTO_EVENTOS dentro do bot.py.
🔮 Possíveis Melhorias Futuras
Conectar o bot a um banco de dados (como PostgreSQL ou SQLite) em vez de um arquivo Excel, para maior escalabilidade e performance.
Expandir o MAPEAMENTO_EVENTOS com mais feriados ou eventos customizados.
Adicionar suporte para feriados estaduais, passando o parâmetro subdiv='SP' (por exemplo) para a biblioteca holidays.
Criar comandos mais complexos, como "faturamento do último mês" ou "comparativo entre dois dias".
📄 Licença
Este projeto está sob a licença MIT.